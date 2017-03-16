/**
 * Load controllers for build template page
 */
$(document).ready(function() {
	$('.btn.save-template').on('click', saveTemplate);
	$('.btn.save-type').on('click', saveType);

	// new template: offer to rename root type
	var $templateID = $("#templateID");
	if ($templateID.html() == "new"){
        displayNewTemplateDialog();
    }
});


/**
 * Save a composed template
 */
var saveTemplate = function(){
	$("#new-template-error").html("");
	$("#save-template-modal").modal("show");
	$("#save-template").on("click", save_template);
};

/**
 * AJAX call, saves a template
 */
var save_template = function(){
    var templateName = $("#newTemplateName").val();

    if (templateName.length > 0){
        $.ajax({
            url : saveTemplateUrl,
            type : "POST",
            dataType: "json",
            data:{
                templateName: templateName
            },
            success: function(data){
                $("#save-success-modal").modal("show");
                $("#save-template-modal").modal("hide");
            },
            error: function(data){
                $("#new-template-error").html("Not a valid XML schema." + data.responseText);
            }
        });
    }else{
        $( "#new-template-error" ).html("The name can't be empty.")
    }
};


/**
 * Save a composed type
 */
var saveType = function(){
	$("#new-type-error").html("");
    $("#save-type-modal").modal("show");
	$("#save-type").on("click", save_type);
};


/**
 * AJAX call, saves a type
 */
var save_type = function(){
    var typeName = $("#newTypeName").val();
    var templateID = $("#templateID").html();
    if (typeName.length > 0){
        $.ajax({
            url : saveTypeUrl,
            type : "POST",
            dataType: "json",
            data:{
                typeName: typeName,
                templateID: templateID
            },
            success: function(data){
                $("#save-success-modal").modal("show");
                $("#save-type-modal").modal("hide");
            },
            error: function (data) {
                $("#new-type-error").html(data.responseText);
            }
        });
    }else{
        $( "#new-type-error" ).html("The name can't be empty.")
    }
};


/**
 * Dialog to change root type name when new template
 */
var displayNewTemplateDialog = function(){
    $( "#newTemplateTypeNameError" ).html("");
    $( "#root-type-name-modal" ).modal("show");
    $( "#rename-root-type").on('click', changeRootTypeName);
};


/**
 * Change the name of root type
 */
var changeRootTypeName = function(){
    var $newRootName = $("#newRootName");
    var $newRootNameError = $("#newRootNameError");

    if ($newRootName.val() == ""){
        // name can not be empty
        $newRootNameError.html("The name can't be empty.");
    }else if (!$newRootName.val().match(/^[a-zA-Z]*$/)){
        // name can only be letters
        $newRootNameError.html("The name can only contains letters.");
    }else{
        var typeName = $newRootName.val();
        change_root_type_name(typeName);
        $( "#root-type-name-modal" ).modal("hide");
    }
};

/**
 * AJAX call, change the name of the root type
 * @param typeName name of the root type
 */
var change_root_type_name = function(typeName){
    $.ajax({
        url : changeRootTypeNameUrl,
        type : "POST",
        dataType: "json",
        data:{
        	typeName: typeName
        },
        success: function(){
            // set the type name
            $("#xsd_form").find(".type").html(typeName);
        }
    });
};
