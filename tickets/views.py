from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from collections import deque
from datetime import datetime
import pdb


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


def ShowMenu(request):
    return render(request, 'tickets/menu.html')


def InflateTires(request):
    #some stuff
    data = the_que.inflation_invoked()
    return render(request, 'tickets/show_queue_content.html', context={'que': data})


def ChangeOil(request):
    data = the_que.oil_invoked()
    return render(request, 'tickets/show_queue_content.html', context={'que': data})


def Diagnostic(request):
    data = the_que.diagnostic_invoked()
    return render(request, 'tickets/show_queue_content.html', context={'que': data})

class TheQueueWorking():
    def __init__(self):
        # self.line_of_cars = {'oil': deque(), 'tires': deque(), 'diagnostic': deque()}
        self.oil = deque()
        self.tires = deque()
        self.diagnostic = deque()
        self.current_ticket = 1

    def oil_invoked(self):
        res = {}
        res['minutes'] = self.calculate_oil_time_in_queue()
        res['position'] = self.get_the_position_in_queue()
        ticket_number = self.calculate_new_ticket_number()
        self.oil.append(ticket_number)
        return res

    def inflation_invoked(self):
        res = {}
        res['minutes'] = self.calculate_inflation_time_in_queue()
        res['position'] = self.get_the_position_in_queue()
        ticket_number = self.calculate_new_ticket_number()
        self.tires.append(ticket_number)
        return res

    def diagnostic_invoked(self):
        res = {}
        res['minutes'] = self.calculate_diagnostic_time_in_queue()
        res['position'] = self.get_the_position_in_queue()
        ticket_number = self.calculate_new_ticket_number()
        self.diagnostic.append(ticket_number)
        return res

    def calculate_oil_time_in_queue(self):
        oil = self.get_oil_minutes()
        return oil

    def calculate_inflation_time_in_queue(self):
        oil = self.get_oil_minutes()
        inflate = self.get_inflate_minutes()
        return oil + inflate

    def calculate_diagnostic_time_in_queue(self):
        oil = self.get_oil_minutes()
        inflate = self.get_inflate_minutes()
        diagnostic = self.get_diagnostic_minutes()
        return oil + inflate + diagnostic

    def get_oil_minutes(self):
        return len(self.oil) * 2

    def get_inflate_minutes(self):
        return len(self.tires) * 5

    def get_diagnostic_minutes(self):
        return len(self.diagnostic) * 30

    def get_the_position_in_queue(self):
        current_queue_length = len(self.oil) + \
                               len(self.tires) + \
                               len(self.diagnostic)
        return current_queue_length + 1

    def get_current_ticket_and_pop(self):
        res = 0
        if len(self.oil) > 0:
            res = self.oil.popleft()
        elif len(self.tires) > 0:
            res = self.tires.popleft()
        elif len(self.diagnostic) > 0:
            res = self.diagnostic.popleft()

        return res

    def calculate_new_ticket_number(self):
        res = self.current_ticket
        self.current_ticket += 1
        return res


def OperatorInterface(request):
    if request.method == 'POST':
        make_an_action()
        return redirect('/next')
    data = GetNumbersForOperator()
    return render(request, 'tickets/operator_interface.html', context={'data': data})


def GetNumbersForOperator():
    data = {}
    data['oil_len'] = len(the_que.oil)
    data['tires_len'] = len(the_que.tires)
    data['diagnostic_len'] = len(the_que.diagnostic)
    return data


def make_an_action():
    global current_ticket
    closest_ticket = the_que.get_current_ticket_and_pop()
    if closest_ticket != 0:
        current_ticket = closest_ticket


def process_next(request):

    global current_ticket

    if current_ticket == 'Waiting for the next client':
        return render(request, 'tickets/next_client_is_awaited.html')
    else:
        return render(request, 'tickets/customers_page.html',
                      context={'ticket_number': current_ticket})


the_que = TheQueueWorking()
current_ticket = 'Waiting for the next client'

