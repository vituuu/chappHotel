from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date

class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    price = models.FloatField(null=False, blank=False, default=50.0)
    peopleMax = models.IntegerField (null=False, blank=False, default=1)
    description = models.CharField(max_length = 200)

    @staticmethod
    def getRoom(roomId):
        return Room.objects.get(id = roomId)

    def __str__(self):
        return 'Room number: ' + str(self.id) + ' Habitability:' + str(self.peopleMax) + ' people'


class Booking(models.Model):
    CONFIRMADA = 'conf'
    CHECKIN = 'cIn'
    CHECKOUT = 'cOut'
    CANCELED = 'canc'
    STATUS = [
        (CONFIRMADA, 'confirmada'),
        (CHECKIN, 'checkin'),
        (CHECKOUT, 'checkout'),
        (CANCELED, 'canceled'),
    ]

    checkInDate  = models.DateField(auto_now=False)
    checkOutDate = models.DateField(auto_now=False)
    creationDate = models.DateField(auto_now=True)
    status = models.CharField(max_length=4,
                              choices=STATUS,
                              default=CONFIRMADA)
    room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
    )
    people      = models.IntegerField(null=False, 
                               blank=False, 
                               default=2)
    client      = models.ForeignKey(User, on_delete=models.CASCADE)
    
    telephone   = models.CharField(max_length=20)
    creditCard  = models.CharField(max_length=20)

    comments    = models.CharField(max_length=500, null=True)
    price       = models.IntegerField(default=0)

    @staticmethod
    def getAvailableRooms(checkIn, checkOut, people):
        return Room.objects.filter(peopleMax__gte = people).\
                                exclude(Q(booking__checkInDate__range = (checkIn, checkOut)) |\
                                        Q(booking__checkOutDate__range = (checkIn, checkOut)))
        

    @staticmethod
    def getAllBookings():
        return Booking.objects.all()

    @staticmethod
    def cancelBooking(bookingId):
        booking = Booking.objects.get(id = bookingId)
        booking.status = Booking.CANCELED
        booking.save()


    @staticmethod
    def doCheckIn(bookingId):
        booking = Booking.objects.get(id = bookingId)
        booking.status = Booking.CHECKIN
        booking.save()


    @staticmethod
    def doCheckOut(bookingId):
        booking = Booking.objects.get(id = bookingId)
        booking.status = Booking.CHECKOUT
        booking.save()

    @staticmethod
    def getTodayBookings():
        bookings = Booking.objects.filter(Q(checkInDate = (date.today())) |\
                                 Q(checkOutDate = (date.today())))
        return bookings

    def getUserBookings(user):
        return Booking.objects.filter(client = user)

    def performBook(request):
        booking = Booking()
        booking.telephone       = request.POST.get('telephone')
        booking.creditCard      = request.POST.get('creditCard')
        booking.comments        = request.POST.get('comments')
        booking.checkInDate     = datetime.datetime.strptime(request.session['checkIn'], "%d-%m-%Y").date()
        booking.checkOutDate    = datetime.datetime.strptime(request.session['checkOut'], "%d-%m-%Y").date()
        booking.people          = request.session['people']
        booking.room_id         = request.session['roomId']
        booking.client_id       = request.user.id
        booking.price           = booking.room.price*(booking.checkOutDate-booking.checkInDate).days
        
        booking.save()

        return booking

    def __str__(self):
        return 'CheckIn: ' + str(self.checkInDate) + ' Num. of People: ' + str(self.people)


class Guest(models.Model):
    firstName = models.CharField(max_length = 100)
    lastName  = models.CharField(max_length = 100)
    book      = models.ForeignKey(Booking,on_delete=models.CASCADE)


    def storeGuestsNames(request):
        name = request.POST.get('name1','none')
        numOfPeople = int(request.POST.get('numOfPeople','none'))
        bookId = int(request.POST.get('bookingId','none'))
        for i in range(1,numOfPeople+1):
            name =  request.POST.get('name' + str(i),'none')   
            surname = request.POST.get('surname' + str(i),'none')   
            Guest(firstName = name, lastName = surname, book_id = bookId).save()


    def __str__(self):
        return self.firstName + self.lastName
