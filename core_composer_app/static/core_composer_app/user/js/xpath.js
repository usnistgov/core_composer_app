/**
 * Builds xpath of selected element
 * @returns
 */
var getXPath = function(target){
    var $target = $(target);
	var current = $target.parent().siblings('.path');
	var xpath = $(current).text();
	current = $(current).parent().parent().parent().siblings('.path');
	while(current != null){
		var current_path = $(current).text() ;
		if (current_path.indexOf("schema") != -1){
			current = null;
		}else{
			xpath = current_path + "/" + xpath;
			current = $(current).parent().parent().parent().siblings('.path');
		}
	}
	return xpath;
};

/**
 * Updates elements xpath before suppression
 */
var manageXPath = function(target){
    var $target = $(target);
    var $path = $($target.parent().siblings('.path'));
	var xpath = $path.text();
	var namespace = xpath.split(":")[0];
	var i = 1;
	$target.closest("ul").children().each(function(){
        if(!($(this).find(".path").html() == $target.closest("li").find(".path").html() )){
            $(this).find(".path").html(namespace + ":element["+i+"]");
            i += 1;
        }
	})
};