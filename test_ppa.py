from playwright.sync_api import sync_playwright, Page, expect
import pytest
from time import sleep
import allure

credentials = [('standard_user','secret_sauce'),
            #    ('locked_out_user','secret_sauce'),
            #    ('problem_user','secret_sauce'),
            #    ('performance_glitch_user','secret_sauce'),
            #    ('error_user','secret_sauce'),
            #    ('visual_user','secret_sauce')
               ]

@allure.title('SauceDemo test')
@allure.description('test ini dilakukan dengan nervous')
@allure.severity('minor ')
@allure.label('owner','Pak Diddy')

@pytest.mark.parametrize('Username,Password',credentials)
def test_login_sd(page:Page, Username,Password):
    with allure.step("membuka website"):
        # browser membuka page.
        page.goto('https://saucedemo.com')
        sleep(2)

    with allure.step('input credentials'):
        page.get_by_role('textbox', name='Username').fill(Username)
        page.get_by_role('textbox', name='Password').fill(Password)
        page.get_by_role('button',name='login').click()
        sleep(2)

    with allure.step('assertion inventory page'):
        # assertion inventory page
        expect(page).to_have_url('https://www.saucedemo.com/inventory.html')

    with allure.step('sort option'):
        # sort option dari harga rendah ke tinggi
        dropdown = page.locator("//select[@class='product_sort_container']")
        dropdown.select_option("Price (low to high)")
    
    with allure.step('tambahkan item ke keranjang'):  
        # menambahkan item ke keranjang
        page.locator("//button[@id='add-to-cart-sauce-labs-onesie']").click()

    with allure.step('click buttong menuju keranjang'):
        # klik button menuju keranjang
        page.locator("//a[@class='shopping_cart_link']").click()

    with allure.step('assertion halaman keranjang'):
        # assertion halaman keranjang
        expect(page).to_have_url('https://www.saucedemo.com/cart.html')

    with allure.step('click checkout button'):
        # klik checkout button
        page.locator("//button[@id='checkout']").click()  

    with allure.step('fill order information'):
        # fill order information
        page.locator("//input[@id='first-name']").fill('Pak')
        page.locator("//input[@id='last-name']").fill('Diddy')
        page.locator("//input[@id='postal-code']").fill('666')
        page.locator("//input[@id='continue']").click()

    with allure.step('assertion 2nd checkout phase'):
        # assertion 2nd checkout phase
        expect(page).to_have_url('https://www.saucedemo.com/checkout-step-two.html')
    
    with allure.step('assertion item total'):
        # assertion item total
        item_total = page.locator("//div[@class='summary_subtotal_label']").text_content()
        assert item_total == "Item total: $7.99"

    with allure.step('click finish button'):
        # klik finish button
        page.locator("//button[@id='finish']").click()

    with allure.step('assertion checkout complete'):
        # assertion checkout complete
        expect(page).to_have_url('https://www.saucedemo.com/checkout-complete.html')

    with allure.step('click back to product'):
        # klik back to product
        page.locator("//button[@id='back-to-products']").click()
    
    with allure.step('Screenshot'):
        skrinsut = page.screenshot()
        allure.attach(skrinsut, "page screenshoot", attachment_type= allure.attachment_type.PNG)

    with allure.step('close the page'):
        # close the page/browser
        page.close()
    