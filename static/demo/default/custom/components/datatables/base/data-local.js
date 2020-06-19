//== Class definition

var DatatableDataLocalDemo = function () {
	//== Private functions

	// demo initializer
	var demo = function () {

		var dataJSONArray = JSON.parse('[{"Products":"https://ardiaqa.vteximg.com.br/arquivos/ids/224990-210-210/Cerveza-Miller-en-Lata-473-ml-_1.jpg?v=637224095687100000","Name":"Canned Miller Beer 473 ml.","Brand":"MILLER","OldPrice":"$83.29","Price":"$70.79","Discount":"20%","Supermarket":"https://logos-download.com/wp-content/uploads/2016/05/Dia_logo_red-700x238.png","Type":2}]');

		var datatable = $('.m_datatable').mDatatable({
			// datasource definition
			data: {
				type: 'local',
				source: dataJSONArray,
				pageSize: 10
			},

			// layout definition
			layout: {
				theme: 'default', // datatable theme
				class: '', // custom wrapper class
				scroll: false, // enable/disable datatable scroll both horizontal and vertical when needed.
				// height: 450, // datatable's body's fixed height
				footer: false // display/hide footer
			},

			// column sorting
			sortable: true,

			pagination: true,

			search: {
				input: $('#generalSearch')
			},

			// inline and bactch editing(cooming soon)
			// editable: false,

			// columns definition
			columns: [{
				field: "Products",
				title: "Products",
				template: function (row) {
					return '<img src="'+row.Products+'" width="110px" height="110px" alt="--Product--">';
				}
			}, {
				field: "Name",
				title: "Name",
				responsive: {visible: 'lg'}
			}, {
				field: "Brand",
				title: "Brand"
			}, {
				field: "OldPrice",
				title: "Old Price",
				responsive: {visible: 'lg'},
				template: function (row) {
					return '<div class="oldprice_decoration">'+row.OldPrice+'</div>';
				}
			}, {
				field: "Price",
				title: "Price",
				template: function (row) {
					return '<div class="currentprice_decoration">'+row.Price+'</div>';
				}
			}, {
				field: "Discount",
				title: "Discount",
				// type: ""
			}, {
				field: "Supermarket",
				title: "Supermarket",
				width: "130px",
				template: function (row) {
					return '<img src="'+row.Supermarket+'" width="120px" height="40px" alt="--Product--">';
				}
			},{
				field: "Actions",
				width: 110,
				title: "Actions",
				sortable: false,
				overflow: 'visible',
				template: function (row, index, datatable) {
					var dropup = (datatable.getPageSize() - index) <= 4 ? 'dropup' : '';

					return '\
						<a href="#" class="btn btn-outline-info m-btn m-btn--icon m-btn--icon-only m-btn--custom m-btn--pill" data-toggle="modal" data-target="#m_modal_2" title="Remove from favourites">\
                            <i class="fa fa-trash-o"></i>\
                        </a>\
					';
				}
			}]
		});

		var query = datatable.getDataSourceQuery();

		$('#m_form_status').on('change', function () {
			datatable.search($(this).val(), 'Status');
		}).val(typeof query.Status !== 'undefined' ? query.Status : '');

		$('#m_form_type').on('change', function () {
			datatable.search($(this).val(), 'Type');
		}).val(typeof query.Type !== 'undefined' ? query.Type : '');

		$('#m_form_status, #m_form_type').selectpicker();

	};

	return {
		//== Public functions
		init: function () {
			// init dmeo
			demo();
		}
	};
}();

jQuery(document).ready(function () {
	DatatableDataLocalDemo.init();
});