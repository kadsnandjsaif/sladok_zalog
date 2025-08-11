// CSS-анимация монет подключена в style.css (@keyframes coin-float)

// Плавное появление карточек секции loans и легкий параллакс фона
$(function(){
  var $cards = $('.loan-card');
  // Появление карточек
  $cards.each(function(i){
    var $card = $(this);
    setTimeout(function(){
      $card.animate({opacity: 1, top: 0}, 700, 'swing');
    }, i * 180);
  });

  // Отключаем движение фоновых изображений по требованию
  $('.loan-card__bg').each(function(){ $(this).stop(true, true).css('top', 0); });
});

// Estate: два интерфейса. Desktop — грид. ≤1200 — slick со слайдами .estate-card
$(function(){
  var $grid = $('.estate-grid');
  if (!$grid.length) return;
  var $slider = null;

  function buildSlider(){
    if ($slider) return;
    $slider = $('<div class="estate-slider"/>');
    // Клонируем только карточки как отдельные слайды
    $grid.find('.estate-card').each(function(){
      $slider.append($(this).clone(true, true));
    });
    $grid.after($slider);
    $grid.hide();
    $slider.slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      variableWidth: true,
      centerMode: false,
      dots: false,
      arrows: false,
      infinite: false,
      speed: 400,
      cssEase: 'ease'
    });
  }

  function destroySlider(){
    if ($slider){
      try { $slider.slick('unslick'); } catch(e){}
      $slider.remove();
      $slider = null;
    }
    $grid.show();
  }

  function update(){
    var isMobileUI = window.matchMedia('(max-width: 1699px)').matches;
    if (isMobileUI) buildSlider(); else destroySlider();
  }

  var t;
  $(window).on('resize', function(){ clearTimeout(t); t = setTimeout(update, 120); });
  update();
});

// Модальное меню: открытие/закрытие, плавный скролл, перенос данных из хедера для мобилки
$(function(){
  var $menu = $('#menu');
  var $panel = $menu.find('.menu-panel');
  var $openBtn = $('.burger-menu');
  if (!$menu.length || !$openBtn.length) return;

  function openMenu(){
    $menu.addClass('is-open').attr('aria-hidden','false');
    $('body').css('overflow','hidden');
    $('.burger-menu').attr('aria-expanded','true');
    // Перенос блоков из хедера в меню на мобильных
    if (window.matchMedia('(max-width: 1200px)').matches){
      var $extra = $panel.find('.menu-extra');
      $extra.empty();
      // Берём текстовые элементы хедера кроме логотипа и кнопки меню
      $('.header-text').each(function(){
        var html = $(this).html();
        $('<div/>', { class:'menu-extra__row', html: html }).appendTo($extra);
      });
    }
  }
  function closeMenu(){
    $menu.removeClass('is-open').attr('aria-hidden','true');
    $('body').css('overflow','');
    $('.burger-menu').attr('aria-expanded','false');
  }

  $openBtn.on('click', function(){
    var expanded = $(this).attr('aria-expanded') === 'true';
    if (expanded){ closeMenu(); $(this).attr('aria-expanded','false'); }
    else { openMenu(); $(this).attr('aria-expanded','true'); }
  });
  $menu.on('click', '[data-menu-close]', closeMenu);

  // Плавная прокрутка и закрытие по клику на пункт меню
  $menu.on('click', '[data-menu-link]', function(e){
    var href = $(this).attr('href');
    if (href && href.startsWith('#')){
      e.preventDefault();
      closeMenu();
      var $target = $(href);
      if ($target.length){
        $('html, body').animate({ scrollTop: $target.offset().top - 16 }, 400);
      }
    }
  });
});

// Глобальная навигация: кнопки "Оставить заявку" и "Рассчитать сумму займа"
$(function(){
  function goToCalc(e){
    e.preventDefault();
    var $target = $('#valuation-calc');
    if ($target.length){
      $('html, body').animate({ scrollTop: $target.offset().top - 16 }, 450);
    }
  }
  // Кнопки в шаге 1
  $(document).on('click', '.step-cta', goToCalc);
  // Кнопка верхняя CTA
  $(document).on('click', '.cta-btn', function(e){
    var withinCalc = $(this).closest('#valuation').length > 0 || $(this).closest('#valuation-calc').length > 0;
    if (!withinCalc){ goToCalc(e); }
  });
  // Кнопка approve "Получить деньги" -> тоже к калькулятору
  $(document).on('click', '.approve-cta', function(e){
    var href = $(this).attr('href') || '';
    if (href.indexOf('#valuation-form') !== -1){ goToCalc(e); }
  });
});

// Анимация появления карточек special при прокрутке
$(function(){
  var items = document.querySelectorAll('.special-card');
  if (!items.length) return;
  items.forEach(function(el){ el.style.opacity = 0; el.style.transform = 'translateY(12px)'; });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (e.isIntersecting){
        e.target.style.transition = 'opacity .3s ease, transform .3s ease';
        e.target.style.opacity = 1; e.target.style.transform = 'translateY(0)';
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.2 });
  items.forEach(function(el){ io.observe(el); });
});

// Появление блоков steps
$(function(){
  var items = document.querySelectorAll('.step');
  if (!items.length) return;
  items.forEach(function(el){ el.style.opacity = 0; el.style.transform = 'translateY(12px)'; });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (e.isIntersecting){
        e.target.style.transition = 'opacity .3s ease, transform .3s ease';
        e.target.style.opacity = 1; e.target.style.transform = 'translateY(0)';
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.15 });
  items.forEach(function(el){ io.observe(el); });
});
// Появление карточек riski
$(function(){
  var items = document.querySelectorAll('.riski-card');
  if (!items.length) return;
  items.forEach(function(el){ el.style.opacity = 0; el.style.transform = 'translateY(12px)'; });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (e.isIntersecting){
        e.target.style.transition = 'opacity .3s ease, transform .3s ease';
        e.target.style.opacity = 1; e.target.style.transform = 'translateY(0)';
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.15 });
  items.forEach(function(el){ io.observe(el); });
});

// Плавное появление элементов probability
$(function(){
  var items = document.querySelectorAll('.probability__left, .probability__right');
  if (!items.length) return;
  items.forEach(function(el){ el.style.opacity = 0; el.style.transform = 'translateY(12px)'; });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (e.isIntersecting){
        e.target.style.transition = 'opacity .35s ease, transform .35s ease';
        e.target.style.opacity = 1; e.target.style.transform = 'translateY(0)';
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.2 });
  items.forEach(function(el){ io.observe(el); });
});

// Маска телефона во всем проекте
$(function(){
  $('.wpcf7-tel').inputmask("+7 (999)-999-99-99");
});

// Калькулятор займа: обновление значений
$(function(){
  var amount = document.getElementById('loanAmount');
  var amountVal = document.getElementById('loanAmountValue');
  var term = document.getElementById('loanTerm');
  var termVal = document.getElementById('loanTermValue');
  if (amount && amountVal){
    var fmt = new Intl.NumberFormat('ru-RU');
    var updateAmount = function(){ amountVal.textContent = fmt.format(parseInt(amount.value,10)) + ' ₽'; };
    amount.addEventListener('input', updateAmount); updateAmount();
  }
  if (term && termVal){
    var updateTerm = function(){ var v = parseInt(term.value,10); termVal.textContent = v + ' ' + (v%10===1 && v%100!==11 ? 'месяц' : (v%10>=2&&v%10<=4 && (v%100<10||v%100>=20) ? 'месяца' : 'месяцев')); };
    term.addEventListener('input', updateTerm); updateTerm();
  }
  // выбранные файлы
  var fileInput = document.querySelector('.file-uploader input[type="file"]');
  var fileOut = document.querySelector('.file-selected');
  if (fileInput && fileOut){
    fileInput.addEventListener('change', function(){
      if (!this.files || this.files.length === 0){ fileOut.textContent = ''; return; }
      var names = Array.from(this.files).map(function(f){ return f.name; });
      fileOut.textContent = 'Прикреплено: ' + names.join(', ');
    });
  }
});

// Slick slider для отзывов
$(function(){
  if ($('.reviews-slider').length){
    var $slider = $('.reviews-slider').slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      variableWidth: true,      // фиксируем ширину карточки в 550px
      centerMode: false,
      dots: false,
      arrows: false,
      infinite: true,
      speed: 400,
      cssEase: 'ease',
      adaptiveHeight: false
    });
    // Кастомные стрелки под слайдером
    // назначаем обработчики на уже вставленные SVG-стрелки
    $('.reviews-arrow--prev').on('click', function(){ $slider.slick('slickPrev'); });
    $('.reviews-arrow--next').on('click', function(){ $slider.slick('slickNext'); });
  }
});

// Fancybox для модалки «Спасибо!»
$(function(){
  if (window.Fancybox) {
    Fancybox.bind('[data-fancybox]', {
      dragToClose: false,
      closeButton: false,
    });
  }

  $('#apply-form').on('submit', function(e){
    e.preventDefault();
    var form = this;

    // базовая валидация
    var valid = true;
    $(form).find('input[required], select[required]').each(function(){
      var el = $(this);
      if (!el.val()) valid = false;
      if (el.attr('type') === 'number') {
        var min = el.attr('min') ? parseFloat(el.attr('min')) : -Infinity;
        var max = el.attr('max') ? parseFloat(el.attr('max')) : Infinity;
        var val = parseFloat(el.val());
        if (isNaN(val) || val < min || val > max) valid = false;
      }
    });

    if (!valid) {
      $(form).find('.apply-hint').css('color', '#ffb4b4');
      return;
    }

    // меняем текст кнопки и показываем модалку
    $('.apply-submit-text').text('Отправить');
    $('#thanks-trigger').trigger('click');
    setTimeout(function(){
      if (window.Fancybox) Fancybox.close();
    }, 2500);
    form.reset();
  });
});

// Пошаговый мастер формы «apply» с Inputmask и Fancybox
$(function(){
  var $apply = $('.apply');
  if ($apply.length === 0) return;

  // контейнер шага
  var $container = $('<div class="apply-wizard" />');
  var $progress = $('<div class="apply-step__progress"><span class="apply-step__num">01</span>/<span class="apply-step__total">05</span> <span class="apply-step__label">Срок займа</span></div>');
  var $fieldline = $('<div class="apply-fieldline" />');
  var $input = $('<input class="apply-big-input" type="text" autocomplete="off" />');
  var $unit = $('<span class="apply-big-unit"></span>');
  var $hint = $('<small class="apply-hint"></small>');
  var $btn = $('<button type="button" class="cta-btn apply-next" disabled><span class="apply-next-text">Далее</span><span class="cta-arrow">→</span></button>');
  $fieldline.append($input, $unit);
  $container.append($progress, $fieldline, $hint, $('<div class="apply-actions"/>').append($btn));
  $apply.find('.wrapper').append($container);

  var steps = [
    {key:'term', label:'Срок займа', unit:'мес', hint:'от 1 до 120 месяцев', mask:{ alias:'numeric', digits:0, min:1, max:120, rightAlign:false, groupSeparator:' ', autoGroup:false, showMaskOnHover:false, showMaskOnFocus:false }, inputmode:'numeric'},
    {key:'amount', label:'Желаемая сумма займа', unit:'₽', hint:'минимум 50 000', mask:{ alias:'numeric', digits:0, min:50000, rightAlign:false, groupSeparator:' ', autoGroup:true, showMaskOnHover:false, showMaskOnFocus:false }, inputmode:'numeric'},
    {key:'pledge', label:'Вид залога', unit:'', hint:'например: коммерческая недвижимость', mask:{ regex:'[A-Za-zА-Яа-яЁё\s\-]{3,60}', showMaskOnHover:false, showMaskOnFocus:false }, inputmode:'text'},
    {key:'income', label:'Заработная плата', unit:'₽', hint:'укажите чистый доход', mask:{ alias:'numeric', digits:0, min:0, rightAlign:false, groupSeparator:' ', autoGroup:true, showMaskOnHover:false, showMaskOnFocus:false }, inputmode:'numeric'},
    {key:'phone', label:'Номер телефона', unit:'', hint:'формат +7 (999)-999-99-99', mask:{ mask:'+7 (999)-999-99-99' }, inputmode:'tel'}
  ];

  var state = {}; var i = 0;

  function setMask(st){
    Inputmask.remove($input[0]);
    if (st.key === 'phone') {
      $input.inputmask(st.mask.mask);
    } else if (st.mask.alias === 'numeric') {
      Inputmask(st.mask).mask($input[0]);
    } else if (st.mask.regex) {
      Inputmask(st.mask).mask($input[0]);
    }
  }

  function render(){
    var st = steps[i];
    $apply.find('.apply-step__num').text(String(i+1).padStart(2,'0'));
    $apply.find('.apply-step__total').text(String(steps.length).padStart(2,'0'));
    $apply.find('.apply-step__label').text(st.label);
    $unit.text(st.unit);
    $hint.text(st.hint);
    $input.attr('inputmode', st.inputmode || 'text').val(state[st.key] || '');
    setMask(st);
    toggle();
    $('.apply-next-text').text(i === steps.length-1 ? 'Отправить' : 'Далее');
  }

  function valid(){
    var st = steps[i]; var v = ($input.val()||'').trim();
    if (!v) return false;
    if (st.key === 'pledge') return /^[A-Za-zА-Яа-яЁё\s\-]{3,60}$/.test(v);
    if (st.key === 'phone') return $input.inputmask('isComplete');
    if (st.mask && st.mask.alias === 'numeric'){
      var n = parseInt(v.replace(/\s+/g,''),10);
      if (isNaN(n)) return false;
      if (st.mask.min!=null && n < st.mask.min) return false;
      if (st.mask.max!=null && n > st.mask.max) return false;
    }
    return true;
  }

  function toggle(){ $btn.prop('disabled', !valid()); }
  function autoWidth(){
    // динамический размер инпута под содержимое
    var span = $('#__measure');
    if (span.length === 0) span = $('<span id="__measure" />').css({position:'absolute', visibility:'hidden', whiteSpace:'pre', fontFamily:'"Druk Cyrillic"', fontWeight:900, fontSize:'56px'}).appendTo(document.body);
    span.text($input.val() || '');
    var w = span.width() + 24;
    $input.css('width', Math.min(Math.max(w, 120), 900));
  }
  $input.on('input keyup', function(){ toggle(); autoWidth(); });

  $btn.on('click', function(e){
    e.preventDefault();
    if (!valid()) return false;
    state[steps[i].key] = $input.val().trim();
    if (i < steps.length-1){
      i++; $container.fadeOut(120, function(){ render(); autoWidth(); $container.fadeIn(120); });
    } else {
      if (window.Fancybox){
        Fancybox.show([{ src:'#thanks-modal', type:'inline' }], { closeButton:false, dragToClose:false });
        setTimeout(function(){ Fancybox.close(); }, 2500);
      }
      i = 0; state = {}; render();
    }
    return false;
  });

  render(); autoWidth();
});

// FAQ аккордеон с активным нижним пунктом и плавным раскрытием
$(function(){
  var $faq = $('.faq');
  if (!$faq.length) return;

  // Инициализация: вычисляем высоты ответов и закрываем все, кроме .is-open
  $('.faq-item').each(function(){
    var $item = $(this);
    var $a = $item.find('.faq-a');
    if ($item.hasClass('is-open')){
      // раскрыт по умолчанию: выставляем авто-высоту
      $a.css('maxHeight', $a.prop('scrollHeight') + 'px');
    } else {
      $a.attr('hidden', true).css('maxHeight', 0);
    }
  });

  $('.faq-q').on('click', function(){
    var $btn = $(this);
    var $item = $btn.closest('.faq-item');
    var $panel = $item.find('.faq-a');
    var isOpen = $item.hasClass('is-open');

    // закрываем остальные
    $('.faq-item.is-open').not($item).each(function(){
      var $it = $(this);
      $it.removeClass('is-open').find('.faq-q').attr('aria-expanded', 'false');
      var $p = $it.find('.faq-a');
      $p.attr('hidden', true).css('maxHeight', 0);
    });

    if (isOpen){
      $item.removeClass('is-open');
      $btn.attr('aria-expanded', 'false');
      $panel.attr('hidden', true).css('maxHeight', 0);
    } else {
      $item.addClass('is-open');
      $btn.attr('aria-expanded', 'true');
      $panel.removeAttr('hidden');
      // выставляем точную высоту контента для плавности
      $panel.css('maxHeight', $panel.prop('scrollHeight') + 'px');
    }
  });
});

// Features: два интерфейса. Desktop — грид. ≤1200 — slick со слайдами .feature
$(function(){
  var $grid = $('.features-grid');
  if (!$grid.length) return;
  var $slider = null;

  function buildFeaturesSlider(){
    if ($slider) return;
    $slider = $('<div class="features-slider"/>');
    $grid.find('.feature').each(function(){
      $slider.append($(this).clone(true, true));
    });
    $grid.after($slider);
    $grid.hide();
    $slider.slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      variableWidth: true,
      centerMode: false,
      dots: false,
      arrows: false,
      infinite: false,
      speed: 400,
      cssEase: 'ease'
    });
  }

  function destroyFeaturesSlider(){
    if ($slider){
      try { $slider.slick('unslick'); } catch(e){}
      $slider.remove();
      $slider = null;
    }
    $grid.show();
  }

  function update(){
    var isSlider = window.matchMedia('(max-width: 1199px)').matches;
    if (isSlider) buildFeaturesSlider(); else destroyFeaturesSlider();
  }

  var t;
  $(window).on('resize', function(){ clearTimeout(t); t = setTimeout(update, 120); });
  update();
});
