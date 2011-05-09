planHandler = {
	init: function(projectId, baseUrl) {
		this.projectId = projectId;
		this.baseUrl = baseUrl.replace('/static','');
		var self = this;
		$('#week_options').change(function() {
		    self.load($(this).val());
		})	
	},
	load: function(weekId) {
		var planUrl = this.baseUrl + 'api/projects/' + this.projectId + "/plans/" + weekId;
		var taskUrl = this.baseUrl + 'api/projects/' + this.projectId + "/tasks/" + weekId;

    $('#plan .editable').html('');
		$.ajax({
			url: planUrl,
			success: function(data) {
        $.each(data, function (field_name, val) {
          $('#Plan-' + field_name).html(val);
        });
        $('input#current-plan-id').val(data['id']);
			}
		});

		$.ajax({
			url: taskUrl,
			success: function(data) {
				$.each(data, function(idx, obj) {
          $.each(obj, function (field_name, val) {
            $('#Task-' + obj.day + '-' + field_name).html(val);
          });
				})
			}
		})
	}
}
