$(document).ready(function () {

  $("#dialog-confirm").dialog({
    modal: true,
    bgiframe: true,
    width: 600,
    height: 200,
    autoOpen: false
  });

  $(".confirm").click(function (e) {
    e.preventDefault();
    var hrefAttribute = $(this).attr("href");

    $("#dialog-confirm").dialog('option', 'buttons', {
      "OK": function () {
        window.location.href = hrefAttribute;
      },
      "Cancel": function () {
        $(this).dialog("close");
      }
    });

    $("#dialog-confirm").dialog("open");

  });

});
