planHandler = {
	init: function(projectId, baseUrl) {
		this.projectId = projectId;
		this.baseUrl = baseUrl.replace('/static','');
		var self = this;
	},
	load: function(weekId, callback, state, loaded) {
		var planUrl = this.baseUrl + 'api/projects/' + this.projectId + "/plans/" + weekId;
		var taskUrl = this.baseUrl + 'api/projects/' + this.projectId + "/tasks/" + weekId;
    var pid = this.projectId;
    var hash = '#plan-tab';

    if (loaded) {
      window.history.pushState('', '', '/projects/' + pid + '/plans/' + weekId + hash); 
      return false;
    }

    $('#plan .editable').html('');
		$.ajax({
			url: planUrl,
			success: function(data) {
        $.each(data, function (field_name, val) {
          $('#Plan-' + field_name).html(val);
        });
        $('input#current-plan-id').val(data['id']);

        $.ajax({
          url: taskUrl,
          success: function(data) {
            $.each(data, function(idx, obj) {
              $.each(obj, function (field_name, val) {
                $('#Task-' + obj.day + '-' + field_name).html(val);
              });
            })
            $('#week_options').val(weekId);
            if (!state) {
              window.history.pushState('', '', '/projects/' + pid + '/plans/' + weekId + hash); 
            }
            callback();
          }
        })

			}
		});

	}
}
