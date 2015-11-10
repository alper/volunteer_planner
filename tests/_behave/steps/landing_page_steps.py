from behave import given, then
import re


@given("I visit the home page")
def impl(context):
    context.browser.get('http://localhost:8000/')


@then('I see the call to action "{call_to_action}" on the page')
def find_cta(context, call_to_action):
    element = context.browser.find_element_by_css_selector("body")
    assert call_to_action in element.text, 'Call to action "%s" was not found' % call_to_action


@then('I see the section "{heading_to_look_for}"')
def find_section(context, heading_to_look_for):
    headings = [h.text for h in
                context.browser.find_elements_by_xpath("//h1 | //h2 | //h3")
                if h.text]
    assert heading_to_look_for in headings


@then('I see a button labeled "{btn_label}"')
def find_button(context, btn_label):
    btn_labels = [btn.text for btn in context.browser.find_elements_by_class_name("btn") if btn.text]
    assert btn_label in btn_labels, 'Cannot find a button with the label "%s"' % btn_label


@then('I see some statistics about the Volunteer Planner')
def find_statistics(context):
    facts_div_containers = context.browser.find_elements_by_class_name('facts')
    stats_div = facts_div_containers[0]

    stats_reg_ex = "(^[0-9]+\n[A-Za-z ]+\n)*(^[0-9]+\n[A-Za-z ]+$)\Z"

    match = re.match(
                stats_reg_ex,
                stats_div.text,
                re.MULTILINE)

    assert match, "Statistics could not be found (regex didnt match)"


@then('I see a list of areas with their respective facilities')
def find_areas_and_facilities(context):
    facts_div_containers = context.browser.find_elements_by_class_name('facts')
    areas_facilities_div = facts_div_containers[1]

    regex_heading = '^.*\n'
    regex_one_area = u'(^[\w ]+\n([\w ]+\u2022)*[\w ]+)'
    regex_at_least_one_area = '(' + regex_one_area + '\n)*' + regex_one_area
    regex_placeholder_msg = 'There are currently no places in need of help.'
    regex_total = regex_heading + '(' + regex_at_least_one_area + '|' + regex_placeholder_msg + ')' + '\Z'

    match = re.match(
                regex_total,
                areas_facilities_div.text,
                re.MULTILINE | re.UNICODE)

    assert match, "Areas and their facilities could not be found (regex didnt match)"


@then('I see a navigation bar in the footer')
def find_nav_bar(context):
    navigation_link_labels = [link.text for link in context.browser.find_elements_by_xpath(
        '//div[@id="footer-nav"]//li//a') if link.text]
    assert navigation_link_labels, 'No navigation bar with links was found'
