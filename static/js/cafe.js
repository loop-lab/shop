(function($) {
    $.fn.redraw = function() {
      return this.map(function(){ this.offsetTop; return this; });
    };
  })(jQuery);

  var Cafe = {
    canPay: true,
    totalPrice: 0,
    products: null,

    init: function() {
      Telegram.WebApp.ready();
      Cafe.products = [
        {
          'id': 1,
          'name': 'Толстовка',
          'files': [
            'sweatshirt_1.png',
            'sweatshirt_2.png',
            'sweatshirt_3.jpg'
          ],
          'sizes': [
            {'id': 1, 'name': '48'},
            {'id': 2, 'name': '50'},
            {'id': 3, 'name': '52'},
            {'id': 4, 'name': '54'},
            {'id': 5, 'name': '56'},
          ],
          'price': 100,
        },
        {
          'id': 2,
          'name': 'Футболка',
          'files': [
            't-shirt_1.png',
            't-shirt_2.png',
            't-shirt_3.jpg'
          ],
          'sizes': [
            {'id': 1, 'name': '48'},
            {'id': 2, 'name': '50'},
            {'id': 3, 'name': '52'},
            {'id': 4, 'name': '54'},
            {'id': 5, 'name': '56'},
          ],
          'price': 75,
        },
      ];

      $('.cafe-items').append(() => {
        html = '';
        Cafe.products.forEach((el) => {
          html +=
            '<div class="cafe-item js-item" data-item-id="' + el.id + '" data-item-price="' + el.price + '">' +
              '<div class="cafe-item-counter js-item-counter">1</div>' +
              '<div class="cafe-item-photo" style="background-image: url(./static/img/' + el.files[0] + ')"></div>' +
              '<div class="cafe-item-label">' +
                '<span class="cafe-item-title">' + el.name + '</span>' +
                '<span class="cafe-item-price">' + el.price + ' coin</span>' +
              '</div>' +
              '<div class="cafe-item-sizes">';

          el.sizes.forEach((size) => {
            html += '<button class="cafe-item-size js-item-size" data-item-size=' + size.id + '>' + size.name + '</button>';
          });

          html += '</div>' +
              '<div class="cafe-item-buttons">' +
                '<button class="cafe-item-decr-button js-item-decr-btn button-item"></button>' +
                '<button class="cafe-item-incr-button js-item-incr-btn button-item"></button>' +
              '</div>' +
            '</div>';
        });
        return html;
      });

      $('body').show();
      $('.js-item-incr-btn').on('click', Cafe.eIncrClicked);
      $('.js-item-decr-btn').on('click', Cafe.eDecrClicked);
      $('.js-item-size').on('click', Cafe.sizeClicked);
      Telegram.WebApp.MainButton.setParams({
        text_color: '#fff',
      }).onClick(Cafe.mainBtnClicked);
    },
    sizeClicked: function(el) {
      el.preventDefault();
      $(this).siblings().removeClass('selected');
      $(this).toggleClass('selected', !$(this).hasClass('selected'));
    },
    incrClicked: function(itemEl, delta) {
      var count = +itemEl.data('item-count') || 0;
      count += delta;
      if (count < 0) {
        count = 0;
      }
      itemEl.data('item-count', count);
      Cafe.updateItem(itemEl, delta);
    },
    eIncrClicked: function(e) {
      e.preventDefault();
      var itemEl = $(this).parents('.js-item');
      Cafe.incrClicked(itemEl, 1);
    },
    eDecrClicked: function(e) {
      e.preventDefault();
      var itemEl = $(this).parents('.js-item');
      Cafe.incrClicked(itemEl, -1);
    },
    updateItem: function(itemEl) {
      var count = +itemEl.data('item-count') || 0;
      var counterEl = $('.js-item-counter', itemEl);
      counterEl.text(count ? count : 1);
      itemEl.toggleClass('selected', count > 0);

      Cafe.updateTotalPrice();
    },
    formatPrice: function(price) {
      return Cafe.formatNumber(price, 0, '.', ',') + ' CTFCoin';
    },
    formatNumber: function(number, decimals, decPoint, thousandsSep) {
      number = (number + '').replace(/[^0-9+\-Ee.]/g, '')
      var n = !isFinite(+number) ? 0 : +number
      var prec = !isFinite(+decimals) ? 0 : Math.abs(decimals)
      var sep = (typeof thousandsSep === 'undefined') ? ',' : thousandsSep
      var dec = (typeof decPoint === 'undefined') ? '.' : decPoint
      var s = ''
      var toFixedFix = function (n, prec) {
        if (('' + n).indexOf('e') === -1) {
          return +(Math.round(n + 'e+' + prec) + 'e-' + prec)
        } else {
          var arr = ('' + n).split('e')
          var sig = ''
          if (+arr[1] + prec > 0) {
            sig = '+'
          }
          return (+(Math.round(+arr[0] + 'e' + sig + (+arr[1] + prec)) + 'e-' + prec)).toFixed(prec)
        }
      }
      s = (prec ? toFixedFix(n, prec).toString() : '' + Math.round(n)).split('.')
      if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep)
      }
      if ((s[1] || '').length < prec) {
        s[1] = s[1] || ''
        s[1] += new Array(prec - s[1].length + 1).join('0')
      }
      return s.join(dec)
    },
    updateMainButton: function() {
      var mainButton = Telegram.WebApp.MainButton;
      mainButton.setParams({
        is_visible: !!Cafe.canPay,
        text: Cafe.formatPrice(Cafe.totalPrice),
        color: '#31b545'
      }).hideProgress();
    },
    updateTotalPrice: function() {
      var total_price = 0;
      $('.js-item').each(function() {
        var itemEl = $(this)
        var price = +itemEl.data('item-price');
        var count = +itemEl.data('item-count') || 0;
        total_price += price * count;
      });
      Cafe.canPay = total_price > 0;
      Cafe.totalPrice = total_price;
      Cafe.updateMainButton();
    },
    getOrderData: function() {
      var order_data = {products: [], total: Cafe.totalPrice};
      $('.js-item').each(function() {
        var itemEl = $(this)
        var id    = itemEl.data('item-id');
        var count = +itemEl.data('item-count') || 0;
        var size = itemEl.find('.cafe-item-size.selected').data('item-size');
        if (count > 0) {
          order_data.products.push({id: id, size: size, count: count});
        }
      });
      return JSON.stringify(order_data);
    },
    mainBtnClicked: function() {
      Telegram.WebApp.sendData(Cafe.getOrderData());
    },
  };
