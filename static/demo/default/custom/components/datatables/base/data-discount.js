//== Class definition

var DatatableDataLocalDemo = function () {
	//== Private functions

	// demo initializer
	var demo = function () {

		var dataJSONArray = JSON.parse('[{"payment_url":"https://www.disco.com.ar/DiscoComprasArchivos/Archivos/478667.jpg","seemore":"Great!!! There will be more discounts... :)","Payment Type":"1","Discount":"20%","Supermarket":"https://logos-download.com/wp-content/uploads/2016/05/Dia_logo_red-700x238.png","Type":1}]');

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
				field: "payment_url",
				title: "Payment Logo",
				template: function (row) {
					return '<img src="'+row.payment_url+'" width="110px" height="80px" alt="--Product--">';
				}
			},{
				field: "Discount",
				title: "Discount",
				template: function (row) {
					return '<div class="discount_decoration">'+row.Discount+' off</div>';
				}
			}, {
				field: "Supermarket",
				title: "Supermarket",
				template: function (row) {
					return '<img src="'+row.Supermarket+'" width="120px" height="40px" alt="--Product--">';
				}
			},{
				field: "seemore",
				title: "Description",
				// type: ""
			},{
				field: "See more",
				width: 110,
				title: "Action",
				sortable: false,
				overflow: 'visible',
				template: function (row, index, datatable) {
					var dropup = (datatable.getPageSize() - index) <= 4 ? 'dropup' : '';

					return '\
						<a href="#" class="btn btn-outline-info m-btn m-btn--icon m-btn--icon-only m-btn--custom m-btn--pill"   data-toggle="modal" data-target="#m_modal_2" title="Remove from favourites">\
                            <i class="flaticon-more-v2"></i>\
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