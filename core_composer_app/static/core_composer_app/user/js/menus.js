/**
 * Selected element in the XSD tree
 */
var target;

/**
 * Loads controllers for menus of build template page
 */
$(document).ready(function() {
    // hide any displayed menu
    $(".options_menu").each(function () {
       $(this).hide();
    });
});


/**
 * Displays menu
 * @param $menu
 * @param event
 */
var showMenu = function($menu, event){
    // hide any displayed menu
    $(".options_menu").each(function () {
       $(this).hide();
    });

    var $menuDiv = $($menu.prop('outerHTML'));
    $menuDiv
        .menu()
        .appendTo("body")
        .position({
            my: "left top",
            at: "left bottom",
            of: event.target
        }).show();

    // delete menu on click outside form
    $(document).on('click', function(event) {
        if (!$(event.target).closest('#xsd_form').length) {
            $menuDiv.remove();
        }
	});
};


/*
 * Shows the menu for the sequence
 */
var showMenuSequence=function(event){

	target = event.target;
	showMenu($("#menu_sequence"), event);
};


/**
 * Displays menu for XSD elements
 * @param event
 */
var showMenuElement=function(event){
	target = event.target;
	var parentPath = $(target).parent().parent().parent().parent().siblings('.path').text();

	// not root element
	if(parentPath.indexOf('schema') > -1){
		showMenu($("#menu_element_root"), event);
	}else{ // root element
        showMenu($("#menu_element"), event);
	}
};


/*
 * Shows dialog to insert element in sequence
 */
var displayInsertElementSequenceDialog = function()
{
    $("#insert-element-modal").modal("show");

    $('#table_types').accordion({
                    header: "h3",
                    collapsible: true,
                    active: false,
                    heightStyle: "content"
                });
};


/**
 * Inserts an element in the XML tree
 * @param event
 */
var insertElementSequence = function(event){
    // change the sequence style
    var parent = $(target).parent();
    if ($(parent).attr('class') == "element"){
        $(parent).before("<span class='collapse'/>");
        $(parent).after("<ul></ul>");
        $(parent).attr('class','category');
    }
    // get information about type to insert
    var insertButton = event.target;
    var typeName = $(insertButton).parent().siblings(':first').text();
    var typeID = $(insertButton).parent().siblings(':first').attr('templateid');
    var namespace = $(target).text().split(":")[0];

    // get element's value xpath
    var path = namespace + ":element";
    var nbElement = $(parent).parent().children("ul").children().length;
    if (nbElement > 0){
        path = namespace + ":element[" + String(nbElement + 1) + "]";
    }

    // get xpath to element
    var xpath = getXPath(target);
    $("#insert-element-modal").modal("hide");

	$.ajax({
        url : insertElementSequenceUrl,
        type : "POST",
        dataType: "json",
        data:{
        	typeID: typeID,
        	xpath: xpath,
        	typeName: typeName,
            namespace: namespace,
            path: path
        },
        success: function(data){
            // add the new element to the html tree
            $(parent).parent().children("ul").append(data.new_element);
        },
        error: function(data){
            $( "#validate-error" ).html(data.responseText);
            $( "#error-modal" ).modal("show");
        }
    });
};


/**
 * Displays delete element dialog
 */
var displayDeleteElementDialog = function()
{
    $("#delete-element-modal").modal("show");
};


/**
 * AJAX call, deletes an element
 */
var delete_element = function(){
    var xpath = getXPath(target);
    $.ajax({
        url : deleteElementUrl,
        type : "POST",
        dataType: "json",
        data:{
        	xpath: xpath
        },
        success: function(data){
            manageXPath(target);
            $(target).parent().parent().parent().remove();
            $("#delete-element-modal").modal("hide");
        }
    });
};


/*
 * Shows dialog to change sequence type
 */
var displayChangeTypeDialog = function()
{
    $("#change-element-type-modal").modal("show");

};


/**
 * AJAX call, changes the type of a element
 */
var change_xsd_type = function(){
    var newType = $("#newXSDtype").val();
    var xpath = getXPath(target);

    $.ajax({
        url : changeXsdTypeUrl,
        type : "POST",
        dataType: "json",
        data:{
        	xpath: xpath,
        	newType: newType
        },
        success: function(data){
            // get value of type to change
            var oldType = $(target).text().split(":")[1];
            // update html text
            $(target).html($(target).html().replace(oldType, newType));
            // update xpath value
            var path = $(target).parent().siblings(".path");
            path.html(path.html().replace(oldType, newType));
            $("#change-element-type-modal").modal("hide");
        }
    });
};


/**
 * Shows dialog to rename an element
 */
var displayRenameElementDialog = function()
{
    // reset error messages
    $("#rename-element-error").html("");
    // set current name
    $("#newElementName").val($(target).parent().siblings('.name').html());
    $("#element-name-modal").modal("show");
};


/**
 * AJAX call, renames an element
 */
var rename_element = function(){
    var newName = $("#newElementName").val();
    if (newName.length > 0){
        var xpath = getXPath(target);
        $.ajax({
            url : renameElementUrl,
            type : "POST",
            dataType: "json",
            data:{
                xpath: xpath,
                newName: newName
            },
            success: function(data){
                // set new name in html tree
                $(target).parent().siblings('.name').html(newName);
                $("#element-name-modal").modal("hide");
            },
            error: function(data){
                // set new name in html tree
                $("#rename-element-error").html(data.responseText)
            }
        });
    }else{
        $( "#rename-element-error" ).html("The name can't be empty.")
    }
};


/**
* Management of the unbounded checkbox
*/
var OnClickUnbounded = function()
{
    var unbounded = $("#unbounded").is(':checked');
    var $maxOccurrences = $("#maxOccurrences");
    if(unbounded)
    {

        $maxOccurrences.prop('disabled', true);
        $maxOccurrences.val("unbounded");
    }
    else
    {
        $maxOccurrences.prop('disabled', false);
        $maxOccurrences.val("");
    }
};


/**
 * Show dialog to set occurrences
 */
var displayOccurrencesElementDialog = function()
{
    // reset errors
    $( "#manage-occurrences-error" ).html("");
    // set occurrences
    var xpath = getXPath(target);
    get_occurrences(xpath);
    // show modal
    $( "#occurrences-modal" ).modal("show");
};


/**
 * AJAX call, gets element occurrences from the server
 * @param xpath
 */
var get_occurrences = function(xpath){
    $.ajax({
        url : getElementOccurrencesUrl,
        type : "POST",
        dataType: "json",
        data:{
        	xpath: xpath
        },
        success: function(data){
            var $minOccurrences = $("#minOccurrences");
            var $maxOccurrences = $("#maxOccurrences");
        	$minOccurrences.val(data.minOccurs);
        	$maxOccurrences.val(data.maxOccurs);

        	if(data.maxOccurs == 'unbounded')
        	{
        	    $maxOccurrences.prop('disabled', true);
        	    $('#unbounded').prop('checked', true);
        	}
        	else
        	{
        	    $maxOccurrences.prop('disabled', false);
        	    $('#unbounded').prop('checked', false);
        	}
        }
    });
};


/**
 * Set element occurrences
 */
var setOccurrences = function () {
    var xpath = getXPath(target);
    var minOccurs = $("#minOccurrences").val();
    var maxOccurs = $("#maxOccurrences").val();

    var errors = "";

    if (! isInt(minOccurs)){
        errors += "minOccurs should be an integer.<br/>";
    }else {
        var intMinOccurs = parseInt(minOccurs);
        if (intMinOccurs < 0){
            errors += "minOccurs should be superior or equal to 0.<br/>";
        }
        if (! isInt(maxOccurs)){
            if (maxOccurs != "unbounded"){
                errors += "maxOccurs should be an integer or 'unbounded'.<br/>";
            }
        }else {
            var intMaxOccurs = parseInt(maxOccurs);
            if (intMaxOccurs < 1){
                errors += "maxOccurs should be superior or equal to 1.<br/>";
            }else if (intMaxOccurs < intMinOccurs){
                errors += "maxOccurs should be superior or equal to minOccurs.<br/>";
            }
        }
    }

    if (errors == ""){
        set_occurrences(xpath, minOccurs, maxOccurs);
        $("#occurrences-modal").modal("hide");
    }else{
        $( "#manage-occurrences-error" ).html(errors);
    }
};


/**
 * AJAX call, sets the occurrences of an element
 * @param xpath xpath of the element
 * @param minOccurs minimum occurrences
 * @param maxOccurs maximum occurrences
 */
var set_occurrences = function(xpath, minOccurs, maxOccurs){
    $.ajax({
        url : setElementOccurrencesUrl,
        type : "POST",
        dataType: "json",
        data:{
        	xpath: xpath,
        	minOccurs: minOccurs,
        	maxOccurs: maxOccurs
        },
        success: function(data){
            var occursStr = "( " + minOccurs + " , ";
            if (maxOccurs == "unbounded"){
                occursStr += "*";
            }else{
                occursStr += maxOccurs;
            }
            occursStr += " )";
            $(target).parent().siblings(".occurs").html(occursStr);
        }
    });
};


/**
 * True, if valid integer
 * @param value
 * @returns {boolean}
 */
function isInt(value) {
  return !isNaN(value) && parseInt(Number(value)) == value && !isNaN(parseInt(value, 10));
}

$(document).on('click', '.menu.rename-element', displayRenameElementDialog);
$(document).on('click', '.menu.element-occurrences', displayOccurrencesElementDialog);
$(document).on('click', '.menu.delete-element', displayDeleteElementDialog);
$(document).on('click', '.menu.insert-element', displayInsertElementSequenceDialog);
$(document).on('click', '.menu.change-type', displayChangeTypeDialog);
$(document).on('click', '.menu.element', showMenuElement);
$(document).on('click', '.menu.sequence', showMenuSequence);

$(document).on('click', '.btn.insert', insertElementSequence);
$(document).on('click', '#unbounded', OnClickUnbounded);
$(document).on('click', '#delete-element', delete_element);
$(document).on('click', '#change-element-type', change_xsd_type);
$(document).on('click', '#rename-element', rename_element);
$(document).on('click', '#set-occurrences', setOccurrences);
