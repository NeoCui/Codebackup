function GetLogs(){
	$.ajax({
		url : '/getLog',
		type : 'GET',
		success: function(res){
			var recordObj = JSON.parse(res);
			$('#listTable').bootstrapTable({
				data: recordObj,
				columns : [{
					title: 'Operation',
					field: 'operate',
					align: 'center',
					events: operateEvents,
					formatter: operateFormatter,
				},{
					title: 'ID',
					field: 'Id',
					sortable: true,
				},{
					title: 'Information',
					field: 'Information',
				},{
					title: 'Error Type',
					field: 'Error_Type',
					sortable: true,
				},{
					title: 'Status',
					field: 'Status',
					sortable: true,
				},{
					title: 'Comment',
					field: 'Comment'
				}
				]
			});
		},
		error: function(error){
			alert(error);
		}
	});
}

function operateFormatter(value, row, index){
	return ['<a class="Edit" href="javascript:void(0)" title="Edit">',
		'<i class="glyphicon glyphicon-pencil"></i>',
		'</a> ',
		'<a class="ConfirmDelete" href="javascript:void(0)" title="Delete">',
		'<i class="glyphicon glyphicon-trash"></i>',
		'</a>'].join('');
}

window.operateEvents = {
	'click .Edit': function(e, value, row, index){
		localStorage.setItem('editLogId',row.Id);
		$.ajax({
			url : '/getLogById',
			data : {logid: row.Id},
			type : 'POST',
			success: function(res){
				var data = JSON.parse(res);
				$('#showInfo').val(data[0]['Information']);
				$('#editComment').val(data[0]['Comment']);
				$('#editModal').modal();
			},
			error: function(error){
				alert(error);
			}
		});
	},
	'click .ConfirmDelete': function(e, value, row, index){
		localStorage.setItem('deleteLogId',row.Id);
		$('#deleteModal').modal();
	}
};
function rowStyle(row, index){
	var classes = ['active', 'success', 'info', 'warning', 'danger'];
	if (index%2 == 0){
		return{
			classes: classes[index%5]
		};
	}
	return {};
}
