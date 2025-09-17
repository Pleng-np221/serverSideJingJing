from django import template

register = template.Library()

@register.filter
def sortSectionByDayOfWeek(sections):
    for section in sections:
        section.day_of_week_num = section.dayOfWeek()
    return sections

@register.filter
def formatPhoneNumber(phone_number):
    new_number = phone_number[0:3]+"-"+phone_number[3:7]+"-"+phone_number[7:]
    return new_number