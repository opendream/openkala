
var Breadcrumb = function (bid) {
  self = this;

  var elem = $('#' + bid + ' ul');
  
  self.push = function (title, link) {
    var last = elem.children('li:last');
    last.html('<a href="' + window.location.pathname + window.location.hash + '">' + last.html() + '</a>');
    elem.append('<li>' + title + '</li>')
  }
  self.pop = function (link) {
    elem.children('li:last').remove();
    var last = elem.children('li:last');
    var last_text = last.children('a').html();
    last.html(last_text);

  }
  self.keep = function (n, link) {
    var len = elem.children('li').length;
    elem.children('li').each(function (i, item) {
      if (n <= i) {
        $(this).remove();
      }
    });
    var last = elem.children('li:last');
    var last_text = last.html();
    if (last.children('a').length) {
      last_text = last.children('a').html();
    }
    last.html(last_text);
  }
}
