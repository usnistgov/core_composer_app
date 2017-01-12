//Display dialog to delete a bucket
var deleteBucket = function(){
    var bucket_id = $(this).attr('bucketid');
    $("#bucket_to_delete").html(bucket_id);
	$(function() {
        $( "#dialog-delete-bucket" ).dialog({
            modal: true,
            buttons: {
            	Delete: function() {
            		delete_bucket();
            		$( this ).dialog( "close" );
            		},
				Cancel: function() {
	                $( this ).dialog( "close" );
		          }
		    }
        });
    });
};



//AJAX call, deletes a buckets
var delete_bucket = function(){
    $.ajax({
        url : deleteBucketUrl,
        type : "POST",
        dataType: "json",
        data : {
        	bucket_id : $("#bucket_to_delete").html()
        },
        success: function(data){
            location.reload();
        },
        error: function(data){
        }
    });
};

/**
 * Load controllers for bucket management
 */
$(document).ready(function() {
    $('.delete').on('click', deleteBucket);
});

