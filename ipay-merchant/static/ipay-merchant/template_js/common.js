// Sidebar links
  $('.sidebar .sidebar-menu li a').on('click', function () {
    const $this = $(this);

    if ($this.parent().hasClass('open')) {
      $this
        .parent()
        .children('.dropdown-menu')
        .slideUp(200, () => {
          $this.parent().removeClass('open');
        });
    } else {
      $this
        .parent()
        .parent()
        .children('li.open')
        .children('.dropdown-menu')
        .slideUp(200);

      $this
        .parent()
        .parent()
        .children('li.open')
        .children('a')
        .removeClass('open');

      $this
        .parent()
        .parent()
        .children('li.open')
        .removeClass('open');

      $this
        .parent()
        .children('.dropdown-menu')
        .slideDown(200, () => {
          $this.parent().addClass('open');
        });
    }
  });

  // Sidebar Activity Class
  const sidebarLinks = $('.sidebar').find('.sidebar-link');

  sidebarLinks
    .each((index, el) => {
      $(el).removeClass('active');
    })
    .filter(function () {
      const href = $(this).attr('href');
      const pattern = href[0] === '/' ? href.substr(1) : href;
      return pattern === (window.location.pathname).substr(1);
    })
    .addClass('active');

  // ٍSidebar Toggle
  $('.sidebar-toggle').on('click', e => {
    console.log("clicked");
    $('.app').toggleClass('is-collapsed');
    e.preventDefault();
  });

  /**
   * Wait untill sidebar fully toggled (animated in/out)
   * then trigger window resize event in order to recalculate
   * masonry layout widths and gutters.
   */
  $('#sidebar-toggle').on('click',e => {
    e.preventDefault();
    setTimeout(() => {
      window.dispatchEvent(window.EVENT);
    }, 300);
  });

$('#dataTable').DataTable( {
    responsive: true,
    searching: false,
    paging: false,
    bSort : false,
    paging:   false,
    ordering: false,
    info:     false
} );

$('img').error(function(){
        $(this).attr('src', '/static/ipay-merchant/images/nobody_m.jpg');
});
$(document).ready(function(){
    $('input[name="dateRange"]').daterangepicker();
});

window.scrollTo(0,document.body.scrollHeight);

var qrcode = new QRCode("qrcode");

function makeCode () {
    var elText = document.getElementById("text");

    if (!elText.value) {
        alert("Input a text");
        elText.focus();
        return;
    }

    qrcode.makeCode(elText.value);
}

makeCode();

$("#text").
on("blur", function () {
    makeCode();
}).
on("keydown", function (e) {
    if (e.keyCode == 13) {
        makeCode();
    }
});
