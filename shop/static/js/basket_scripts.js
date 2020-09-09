window.onload = function () {
    $('.cart-table').on('change', 'input[type=number]', function (event) {
        console.log(event.target);
        $.ajax({
            url: '/basket/change/' + event.target.name + '/quantity/' + event.target.value + '/',
            success: function (data) {
                console.log(data)
                $('.cart-table').html(data.result);
                // $('.basket_summary')...
            }
        });
    })
};
