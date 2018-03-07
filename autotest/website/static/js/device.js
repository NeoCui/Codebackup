function GetDevices(){
	$.ajax({
		url : '/getDevice',
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
					title: 'Vendor',
					field: 'Vendor',
					sortable: true,
				},{
					title: 'Description',
					field: 'Description',
				},{
					title: 'Vendorid',
					field: 'Vendorid',
				},{
					title: 'Deviceid',
					field: 'Deviceid',
				},{
					title: 'SubVendorid',
					field: 'Subvendorid',
				},{
					title: 'SubDeviceid',
					field: 'Subdeviceid',
				},{
					title: 'Status',
					field: 'Status',
					sortable: true,
				},{
					title: 'Project',
					field: 'Project',
					sortable: true
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
		localStorage.setItem('editDeviceId',row.Id);
		$.ajax({
			url : '/getDeviceById',
			data : {pciidid: row.Id},
			type : 'POST',
			success: function(res){
				var data = JSON.parse(res);
				$('#showDes').val(data[0]['Description']);
				$('#editVendor').val(data[0]['Vendorid']);
				$('#editDevice').val(data[0]['Deviceid']);
				$('#editSubvendor').val(data[0]['Subvendorid']);
				$('#editSubdevice').val(data[0]['Subdeviceid']);
				$('#editPro').val(data[0]['Project']);
				$('#editModal').modal();
			},
			error: function(error){
				alert(error);
			}
		});
	},
	'click .ConfirmDelete': function(e, value, row, index){
		localStorage.setItem('deleteDeviceId',row.Id);
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
