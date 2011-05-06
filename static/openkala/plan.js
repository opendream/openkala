planHandler = {
	init: function(projectId, baseUrl) {
		console.log('init', arguments);
		this.projectId = projectId;
		this.baseUrl = baseUrl.replace('/static','');
		console.log(this);
		var self = this;
		$('#week_options').change(function() {
		    self.load($(this).val());
		})	
	},
	load: function(weekId) {
		var planUrl = this.baseUrl + 'api/projects/' + this.projectId + "/plans/" + weekId;
		var taskUrl = this.baseUrl + 'api/projects/' + this.projectId + "/tasks/" + weekId;
		console.log(weekId, planUrl, taskUrl);
		$.ajax({
			url: planUrl,
			success: function(data) {
				console.log(data);
				$('#goal')[0].innerHTML = data.goal;
				$('#activity')[0].innerHTML = data.activity;
				$('#sub_topic')[0].innerHTML = data.sub_topic;
				$('#key_thinking')[0].innerHTML = data.key_thinking;
				$('#performance')[0].innerHTML = data.performance;
			}
		});

		$.ajax({
			url: taskUrl,
			success: function(data) {
				console.log(data);
				$.each(data, function(idx, obj) {
					var day = obj.day;
					$.each(['activity', 'source', 'work', 'assessment'], function(idx, name) {
						var f = '#' + name + '-' + day;
						console.log(f);
						$(f)[0].innerHTML = obj[name];
					});
				})
			}

		})
	}
}