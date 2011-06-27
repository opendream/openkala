function photo_upload_build(create) { var input = $('#photo-upload');

  input.change(function(){

    var fileInput = $('#photo-upload');
    var files = fileInput.attr('files');
    var len = files.length
    var count_complete = 0;
    var count_error = 0;

    var pathname = window.location.pathname;

    $.each(files, function (i, file) {
      var xhr = new XMLHttpRequest();

      var progress = $('<div class="photo-progress"></div>').css('width', '0%');
      var bar = $('<div class="photo-bar"></div>').append(progress);
      var detail = $('<div class="photo-detail"></div>').html(file.fileName);
      var current = $('<div class="photo-current"></div>').append(bar).append(detail);
      $('#photo-current-wrap').append(current)

      xhr.upload.onloadstart = function (evt) {
        bar.addClass('uploading');
      };

      xhr.upload.onprogress = function (evt) {
          var percent = evt.loaded/evt.total*100;
          progress.css('width', percent + '%');
      };

      xhr.onreadystatechange = function (e) {
        count_complete++;
        if (count_complete + count_error >= len) {
          gallery_init();
        }
      };

      xhr.onerror = function (evt) {
        count_error++;
      };

      var sync = i == 0? false: true;

      xhr.open('POST', pathname, sync);
      xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
      xhr.setRequestHeader("X-File-Name", file.fileName);
      xhr.setRequestHeader("X-File-Size", file.fileSize);
      xhr.setRequestHeader("X-File-Type", file.type);
      xhr.send(file); // Simple!
      if (!sync) {
        progress.css('width', '100%');
        pathname = xhr.responseText;
      }
    });

  });
}
