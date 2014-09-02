$(document).ready(function () {
  $("#burndownhelpcontent").dialog({
    modal: true,
    bgiframe: true,
    width: 600,
    height: 300,
    autoOpen: false
  });

  $("#burndownhelp").click(function (e) {
    $("#burndownhelpcontent").dialog('option', 'buttons', {
      "OK": function () {
        $(this).dialog("close");
      }
    });

    $("#burndownhelpcontent").dialog("open");
  });

});

$(document).ready(function () {
  $("#categoryhelpcontent").dialog({
    modal: true,
    bgiframe: true,
    width: 600,
    height: 200,
    autoOpen: false
  });

  $("#categoryhelp").click(function (e) {
    $("#categoryhelpcontent").dialog('option', 'buttons', {
      "OK": function () {
        $(this).dialog("close");
      }
    });

    $("#categoryhelpcontent").dialog("open");
  });

});

$(document).ready(function () {
  $("#twodhelpcontent").dialog({
    modal: true,
    bgiframe: true,
    width: 600,
    height: 300,
    autoOpen: false
  });

  $("#twodhelp").click(function (e) {
    $("#twodhelpcontent").dialog('option', 'buttons', {
      "OK": function () {
        $(this).dialog("close");
      }
    });

    $("#twodhelpcontent").dialog("open");
  });

});

$(document).ready(function () {
  $("#headerhelpcontent").dialog({
    modal: true,
    bgiframe: true,
    width: 600,
    height: 300,
    autoOpen: false
  });

  $("#headerhelp").click(function (e) {
    $("#headerhelpcontent").dialog('option', 'buttons', {
      "OK": function () {
        $(this).dialog("close");
      }
    });

    $("#headerhelpcontent").dialog("open");
  });

});

$(document).ready(function () {
  $("#componenthelpcontent").dialog({
    modal: true,
    bgiframe: true,
    width: 600,
    height: 300,
    autoOpen: false
  });

  $("#componenthelp").click(function (e) {
    $("#componenthelpcontent").dialog('option', 'buttons', {
      "OK": function () {
        $(this).dialog("close");
      }
    });

    $("#componenthelpcontent").dialog("open");
  });

});
