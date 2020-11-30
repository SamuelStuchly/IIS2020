import django_filters
from .models import Hotel,Room
from sys import maxsize

class HotelFilter(django_filters.FilterSet):

    class Meta:
        model = Hotel
        fields = {
            'name':['icontains'],
            'stars':['iexact'],
            'city':['icontains']
        }

class RoomFilter(django_filters.FilterSet):

    CHOICES= (
        ('cheap_first','From low to high price'),
        ('expensive_first','From high to low price'),
        ('asc','Bed count asceding'),
        ('desc','Bed count descending')
    )

    RANGES= (
        ('0_to_10','Between 0 and 10'),
        ('10_to_50','Between 10 and 50'),
        ('50_to_100','Between 50 and 100'),
        ('100_to_more','More than 100')
    )

    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')
    price_range = django_filters.ChoiceFilter(label='Price range', choices=RANGES, method='filter_by_price')
    
    class Meta:
        model = Room
        fields = (
            'room_type',
             'beds_number'
        )

    def filter_by_order(self,queryset,name,value):
        
        if value == 'cheap_first':
             expression = 'price' 
        elif value == 'expensive_first':
             expression = '-price' 
        elif value == 'asc':
            expression = 'beds_number' 
        else:
            expression = '-beds_number' 
        
        return queryset.order_by(expression)


    def filter_by_price(self,queryset,name,value):
        
        if value == '0_to_10':
             qset = queryset.filter(price__range=[0,10])
        elif value == '10_to_50':
             qset = queryset.filter(price__range=[10,50])
        elif value == '50_to_100':
            qset = queryset.filter(price__range=[50,100])
        else:
            qset = queryset.filter(price__range=[100,maxsize])
        
        return qset