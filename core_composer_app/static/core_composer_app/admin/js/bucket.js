/**
 * Displays dialog to delete a bucket
 */
var deleteBucket = function(){
    var bucket_id = $(this).attr('bucketid');
    $("#bucket_id").html(bucket_id);
    $("#delete-bucket-modal").modal("show");
};


/**
 * AJAX call, deletes a buckets
 */
var delete_bucket = function(){
    $.ajax({
        url : deleteBucketUrl,
        type : "POST",
        dataType: "json",
        data : {
        	bucket_id : $("#bucket_id").html()
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

$('#delete-bucket').on('click', delete_bucket);
