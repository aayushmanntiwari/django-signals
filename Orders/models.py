import json
from django.db import models
from django.db.models.signals import post_save,post_init
from django.contrib.auth.models import User
from unique_id import get_unique_id
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from Pizza.models import *

# Create your models here.
class Orders(models.Model):
    CHOICES = (
    ("Order Recieved", "Order Recieved"),
    ("Baking", "Baking"),
    ("Baked", "Baked"),
    ("Out for delivery", "Out for delivery"),
    ("Order delivered", "Order delivered")
    )
    order_id = models.CharField(blank=True,null=True,unique=True,max_length=10)
    pizza = models.ForeignKey(Pizza,on_delete=models.CASCADE)
    size = models.ForeignKey(PizzaOptions,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=100,blank=True,null=True,choices=CHOICES,default="Order Recieved")
    curr_total_amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = get_unique_id(length=8)
        if self.quantity!=0 and self.pizza is not None:
            self.curr_total_amount = self.quantity * self.size.amount
        super().save(*args, **kwargs)

    #static method can be callled without instance 
    @staticmethod
    def give_order_details(order_id):
        print('this is called static method ')
        data = {}
        order = Orders.objects.filter(id = order_id).first()
        data['id'] = order.id
        data['order_id'] = order.order_id
        data['total_amount'] = order.curr_total_amount
        data['status'] = order.status
        progress_percentage = 20
        if order.status == 'Order Recieved':
            progress_percentage = 20
        elif order.status == 'Baking':
            progress_percentage = 40
        elif order.status == 'Baked':
            progress_percentage = 60
        elif order.status == 'Out for delivery':
            progress_percentage = 80
        elif order.status == 'Order delivered':
            progress_percentage = 100
        data['progress'] = progress_percentage
        return data
    
    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')
        '''print(instance.id)
        print(instance.previous_state)
        print(instance.status)
        print(created)'''
        if instance.previous_state != instance.status or created: #now we check wheather last status value == new status value if not this condiiton satisfy.
            data = {}
            order = Orders.objects.filter(id = instance.id).first()
            data['id'] = order.id
            data['order_id'] = order.order_id
            data['total_amount'] = order.curr_total_amount
            data['status'] = order.status
            progress_percentage = 20
            if order.status == 'Order Recieved':
                progress_percentage = 20
            elif order.status == 'Baking':
                progress_percentage = 40
            elif order.status == 'Baked':
                progress_percentage = 60
            elif order.status == 'Out for delivery':
                progress_percentage = 80
            elif order.status == 'Order delivered':
                progress_percentage = 100
            data['progress'] = progress_percentage
            #on update order-{}.format(order.id) is the room_group_name of the channel in consumer.py which call the method we declare in type and data you want to send will be in text 
            #In type we write which method you want to call 
            #text contain the json data we want to send
            channels_layer = get_channel_layer()
            print(channels_layer)
            async_to_sync(channels_layer.group_send)(
                'order-{}'.format(order.id),{ 
                    'type':'order_status', 
                    'text':json.dumps(data)
                }
            )

    @staticmethod
    def remember_state(sender, **kwargs):
        instance = kwargs.get('instance')
        instance.previous_state = instance.status #everytime when status field is changed the last field value will be stored


#when we update status field value it will call the post save method and in post save method we are calling the channel layer
post_save.connect(Orders.post_save, sender=Orders)
post_init.connect(Orders.remember_state, sender=Orders)

