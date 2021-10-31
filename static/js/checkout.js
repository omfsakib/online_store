var shipping = '{{order.shipping}}'
    var total = '{{ order.get_cart_total|floatformat:2 }}'

    if (shipping == 'False'){
         document.getElementById('shipping-info').innerHTML = ''
    }

    if(user != 'AnonymousUser'){
        document.getElementById('user-info').innerHTML =''
    }
    if(shipping == 'False' && user != 'AnonymousUser'){
        document.getElementById('form-wrapper').classList.add("hidden");
        document.getElementById('payment-info').classList.remove("hidden");
    }

    var form = document.getElementById('form')
    form.addEventListener('submit', function(e){
        e.preventDefault()
        console.log('Form Submitted...')
        document.getElementById('form-button').classList.add("hidden");
        document.getElementById('payment-info').classList.remove("hidden");
    })

    document.getElementById('make-payment').addEventListener('click', function(e){
        submitFormData()
    })

    function submitFormData(){
        console.log('Payment button clicked')
        var userFormData = {
            'name':null,
            'email':null,
            'total':total,
        }
        var shippingInfo = {
            'address':null,
            'city':null,
            'state':null,
            'zipcode':null,
        }

        if(shipping != 'False'){
            shippingInfo.address = form.address.value
            shippingInfo.city = form.city.value
            shippingInfo.state = form.state.value
            shippingInfo.zipcode = form.zipcode.value
        }

        if(user == 'AnonymousUser'){
            userFormData.name = form.name.value
            userFormData.email = form.email.value
        }

        var url = '/process_order/'
        const request = new Request(
        url,
        {headers: {'Content-Type':'application/json','X-CSRFToken': csrftoken}}
        );
        fetch(request,{
            method:'POST',
            body:JSON.stringify({'form':userFormData,'shipping':shippingInfo
        })
        })
        .then((reponse) => reponse.json())
        .then((data) => {
            console.log('Success:',data);
            alert('Transaction completed');
            window.location.href ="{% url 'store' %}"
        })
    }