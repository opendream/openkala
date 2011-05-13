var ocodes = {};
$(document).ready(function () {

  $('.CoreStandard-code').map(function () { 
    ocodes[$(this).html().trim()] = {
      'jqobj': $(this).parent().next().next().children('.CoreStandard-status').children('.status'), 
      'status':false
    }; 
  });
  
  var build_standard = function (ocodes) {
    var codes = jQuery.extend(true, {}, ocodes);
    var error = [];
    var text = '';
    $('.topic-standard').each(function () { 
      text += ' | ' +  $(this).html(); 
    });

     
      
    text.replace(/([ก-ฮ])\s?(\d*)\.(\d*)\s?:?/g, function(i1, v1, v2, v3) { 
      if (codes[v1 + ' ' + v2 + '.' + v3]) {
        codes[v1 + ' ' + v2 + '.' + v3]['status'] = true;
      }
      else { 
        error.push(v1 + ' ' + v2 + '.' + v3);
      }
    });
      
    $.each(codes, function(cid, code) {
      if (code['status']) {
        code['jqobj'].removeClass('no').addClass('yes').html('ใช่');
      }
      else {
        code['jqobj'].removeClass('yes').addClass('no').html('ไม่ใช่');
      }
    });

    if (error.length) {
      $('.error-message').html('ไม่พบมาตรฐาน' + error.join(', '));
    }
  }

  build_standard(ocodes);

  $('#tab-standard').click(function () {
    build_standard(ocodes);
  });
  
});
