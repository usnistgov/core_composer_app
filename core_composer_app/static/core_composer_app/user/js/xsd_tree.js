/**
 * Shows or hides a section of the XSD tree
 * @param event
 */
var showhide = function(event){
	var button = event.target;
	var parent = $(event.target).parent();
	$(parent.children()[3]).toggle("blind",500);
	if ($(button).attr("class") == "expand"){
		$(button).attr("class","collapse show");
	}else{
		$(button).attr("class","expand");
	}
};

$(document).on('click', '.collapse', showhide);
$(document).on('click', '.expand', showhide);