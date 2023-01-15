from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from store_app.models import Product, Stock, OrderItem, SoldItem, WishListItem, CartItem
from customer_app.models import Customer
    
@receiver(post_save, sender = Product)    
def create_new_stock_item(sender, instance, created, **kwargs):
    print(f'IN CREATE-NEW-STOCK-ITEM...... sender = {sender} instance = {instance} kwargs = {kwargs}')
    if created:
        Stock.objects.create(product= instance)
    instance.stock.save()
    
@receiver(pre_save, sender = OrderItem)
def create_sold_item(sender, instance, **kwargs):
    print(f'IN CREATE-SOLD_ITEM...... sender = {sender} instance = {instance} kwargs = {kwargs}')
    
    stockInfo = Stock.objects.get(product=instance.product)
    print(f"stockInfo = {stockInfo}")
    # solving corner-cases
    if stockInfo.no_of_item_in_stock < instance.quantity:
        print(f"IN IF>>>>>> THROWING EXCEPTION FOR: no_of_stock_item = {stockInfo.no_of_item_in_stock} < instance.quantity = {instance.quantity}")
        raise Exception(f"There is low item quantity of the product {instance.product} in stock.")
    
    # if OrderItem object is being created for first time
    if instance._state.adding:
        print("IN IF(instance._state.adding>>>>>>>>>>>>>)")
        SoldItem.objects.create(
            order=instance.order,
            product=instance.product,
            unit_price=stockInfo.current_unit_price,
            purchase_price=stockInfo.current_purchase_price,
            quantity=instance.quantity,
            discount=stockInfo.current_discount
        )
        print("IN IF(instance._state.adding>>>>>>>>>>>>> FINISHED creating SOLD-ITEM)")
    else: # OrderItem is already created, now it's being updated.
        print("IN ELSE>>>>>>>>>>>>>)")
        soldItemInfo = SoldItem.objects.filter(order=instance.order, product=instance.product).first()
        soldItemInfo.quantity = instance.quantity
        soldItemInfo.save(update_fields=['quantity'])
        print("IN ELSE(instance._state.adding>>>>>>>>>>>>> FINISHED saving SOLD-ITEM-INFO)")
    
@receiver(pre_delete, sender = OrderItem)
def delete_sold_item(sender, instance, **kwargs):
    print(f'IN DELETE-SOLD_ITEM...... sender = {sender} instance = {instance} kwargs = {kwargs}')
    
    soldItemInfo = SoldItem.objects.filter(order=instance.order, product=instance.product).first()
    if soldItemInfo is not None:
        soldItemInfo.delete()
    else:
        raise Exception('No related OrderItem and SoldItem found')
    
@receiver(pre_save, sender=WishListItem)
def validate_wishlist_item_creation(sender, instance, **kwargs):
    wishlist_item_list = instance.customer.wishlistitem_set.all()
    
    # # the above result can be done in this way also
    # customer_info = Customer.objects.filter(pk=instance.customer.id).first()
    # wishlist_item_list = customer_info.wishlistitem_set.all()
    
    for wishlist_item in wishlist_item_list:
        if wishlist_item.product.id == instance.product.id:
            raise Exception("This product is already in the customer's wishlist")
        

@receiver(pre_save, sender=CartItem)
def validate_cart_item(sender, instance, **kwargs):
    if instance.quantity <= 0:
        raise Exception('cannot save cart-item with quantity<=0')