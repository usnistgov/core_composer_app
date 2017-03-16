/**
 * Resolve dependencies
 * @param event
 */
var resolveDependenciesType = function(event)
{
    event.preventDefault();

    var schemaLocations = [];
	var dependencies = [];

	$("#dependencies").find("tr:not(:first)").each(function(){
        var schemaLocation = $(this).find(".schemaLocation").text().trim();
        var dependency = $(this).find(".dependency").val();
        schemaLocations.push(schemaLocation);
        dependencies.push(dependency);
    });

    var xsd_content = $("#xsd_content").html();
    var name = $("#id_name").val();
    var filename = $("#filename").html();
    var version_manager_id = $("#vm_id").html();
    var buckets = $("#id_buckets").val();

    var payload = {
        xsd_content: xsd_content,
        name: name,
        filename: filename,
        version_manager_id: version_manager_id,
        schemaLocations: schemaLocations,
        dependencies : dependencies,
        buckets: buckets
    };
	resolve_dependencies(payload);
};