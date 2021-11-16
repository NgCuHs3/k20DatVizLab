$(document).ready(function() {
   $('body').css({
       visibility: 'visible'
   })
   $('#maintext').addClass('animate__animated animate__fadeInDown')
   
   new Vivus('vaccinesvg', {
    file: './icon/vaccine.svg',
    onReady: function (myVivus) {
      // `el` property is the SVG element
      myVivus.el.setAttribute('height', 'auto');
    }
  });

});



