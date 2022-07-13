var updateBtns = document.getElementsByClassName('update-cart')

for( i = 0; i < updateBtns.length; i++)
{
    updateBtns[i].addEventListener('click',function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId,'Action:',action)
        addCookieItem(productId, action)

    })
}

function updateUserOrder(productId, action) {

    console.log('user is authenticated, sending data')

    var url = '/canteen/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data:', data)
            location.reload()
        });

}

//Guest user
function addCookieItem(productId, action) 
{
    console.log('adding cookies')

    if (action == 'add') 
    {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
        }
        else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') 
    {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('item deleted')
            delete cart[productId];
        }
    }

    if (action == 'delete') 
    {
        delete cart[productId];
    }

    console.log('cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}
var count=0
    for(var i in cart){
        count=count+cart[i]['quantity'];
    }
    console.log(count)
    document.getElementById('cart-total').innerHTML=count;


