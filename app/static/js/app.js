var mic = {
	author: 'Mic',
	version: 1.0
};

mic.display_alert = function (message) {
	var html = '<div class="alert alert-warning alert-dismissible fade in" role="alert"> ';
	html += '<button class="close" type="button" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button>';
	html += '<strong>'+ message +'</strong>';
	html += '</div>';

	return html
};

mic.get_url_params = function (href) {
	href = href.split('?');
	href.shift();
	href = href.join('?');
	href = href.split('&');
	var query = {};
	for (var i=0; i<href.length; i+=1) {
		var q = href[i].split('=');
		query[q[0]] = q[1];
	}
	return query;
};

mic.hook_check_all = function () {
	// 全选 or 反选
	$('input.check-all').bind('click', function() {
		if ($(this).is(':checked')){
			$(this)
				.parents('table')
				.find('.check-one')
				.prop('checked', true);
		} else {
			$(this)
				.parents('table')
				.find('.check-one')
				.prop('checked', false);
		}

		mic.checked_items_status();
	});

	$('input.check-one').click(function () {
		// 取消全选
		if (!$(this).is(':checked')) {
			$('input.check-all')
				.prop('checked', false);
		}
		mic.checked_items_status();
	});
};

mic.hook_delete_all = function () {
	// 删除 全部 or 单个
	$('button.delete-all').click(function () {
		var form_id = $(this).data('form-id');
		swal({
			title: "Confirm to delete?",
			text: "You will not be able to recover the action!",
			type: "warning",
			showCancelButton: true,
			confirmButtonClass: 'btn-warning',
			confirmButtonText: "Yes, delete it!",
			closeOnConfirm: false
		}, function (isConfirm) {
			if (isConfirm) {
				// 检测是否选中
				if ($('#' + form_id).find(':checked').length){
					$('#' + form_id).submit();
				} else {
					swal("Error", "First to selected the one!!!", "error");
				}
			}
		});
	});
};


mic.checked_items_status = function () {
	var total_count = 0;
	$('input.check-one').each(function () {
		if ($(this).is(':checked')) {
			total_count += 1;
		}
	});

	if (total_count > 0) {
		$('.checked-items-status').html(total_count + ' ' + locale_label).removeClass('hidden');
		$('.btn.delete-all').removeClass('hidden');
	} else {
		$('.checked-items-status').addClass('hidden');
		$('.btn.delete-all').addClass('hidden');
	}
};

mic.hook_ajax_modal = function () {
	// 自动绑定ajax的链接
	$('a.ajax-modal').click(function () {
		var url = $(this).attr('href'), modal_name = $(this).data('modal');
		$.get(url, function (html) {
			$('body').append('<div id="'+ modal_name +'" role="dialog" class="modal">' + html + '</div>');

			$('#'+ modal_name).modal('show');
		});
		return false;
	});
};

mic.hook_dropdown_menu = function (callback) {
	$('.dropdown-select-menu .option').on('click', function (cb) {
		var $this=$(this), label=$(this).text(), v=$(this).data('id'),
			target=$(this).parent().parent().data('target');

		$(this)
			.parent()
			.siblings('.active').removeClass('active')
			.end()
			.addClass('active');

		$('input[name='+ target +']').val(v);

		$(this).parent().parent().prev().find('b').text(label);

		callback && callback.call();
	});
};

mic.hook_filter_search = function (callback) {
	$('input.searcher').on('keydown', function (e) {
		var ev = window.event||e;
		if (ev.keyCode == 13) {
			callback && callback.call();
			return false;
		}
	});
};

mic.hook_pjax_link = function () {
	// 导航菜单链接
	$.pjax({
		selector: 'a.pjax',
		container: container_id, //内容替换的容器
		show: 'fade',  //展现的动画，支持默认和fade, 可以自定义动画方式，这里为自定义的function即可。
		cache: false,  //是否使用缓存
		storage: false,  //是否使用本地存储
		titleSuffix: '', //标题后缀
		filter: function(){},
		callback: function(status){
			var type = status.type;
			switch (type) {
				case 'success':
					if ($(this).hasClass('nav-pjax')) {
						$('.sidebar .children a.pjax.active').removeClass('active');
						$(this).addClass('active');
					}
					break;
				case 'error':
					break; //发生异常
			}
		}
	});

	$(document).on('pjax:start', function () {
		NProgress.start();
	});

	$(document).on('pjax:end', function () {
		//加载进度条完成。
		NProgress.done();
		$(container_id).stop(true, true).fadeIn();
	});
};

$(function () {

	$('[data-toggle="tooltip"]').tooltip({
		container: 'body',
		html: true
	});

	$('.select2').select2({
		'width': '100%'
	});

	$('.date').datetimepicker({
		pickTime: false
	});

	$('.alert-dismissable').fadeTo(2000, 500).fadeOut(500, function(){
		$('.alert-dismissable').alert('close');
		$('.flashes').fadeOut(500, function () {
			$(this).remove();
		});
	});

	mic.hook_pjax_link();

	// Image Manager
	$(document).on('click', 'a[data-toggle=\'image\']', function(e) {
		var $element = $(this);
		var $popover = $element.data('bs.popover'); // element has bs popover?
		var $target = $(this).data('target');

		e.preventDefault();

		// destroy all image popovers
		$('a[data-toggle="image"]').popover('destroy');

		// remove flickering (do not re-add popover when clicking for removal)
		if ($popover) {
			return;
		}

		$element.popover({
			html: true,
			placement: 'right',
			trigger: 'manual',
			content: function() {
				return '<button type="button" id="button-image" class="btn btn-primary"><i class="fa fa-pencil"></i></button> <button type="button" id="button-clear" class="btn btn-danger"><i class="fa fa-trash-o"></i></button>';
			}
		});

		$element.popover('show');

		$('#button-image').on('click', function() {
			var $button = $(this);
			var $icon   = $button.find('> i');

			$('#modal-image').remove();

			if ($.cookie('img_last_open_folder') && ($.cookie('img_last_open_folder') != 'undefined')) {
				img_last_open_folder = $.cookie('img_last_open_folder');
			}

			$.ajax({
				url: '/admin/file_manager/show_asset?directory=' + img_last_open_folder + '&up_target=' + $target,
				dataType: 'html',
				beforeSend: function() {
					$button.prop('disabled', true);
					if ($icon.length) {
						$icon.attr('class', 'fa fa-circle-o-notch fa-spin');
					}
				},
				complete: function() {
					$button.prop('disabled', false);
					if ($icon.length) {
						$icon.attr('class', 'fa fa-pencil');
					}
				},
				success: function(html) {
					$('body').append('<div id="modal-image" class="modal">' + html + '</div>');

					$('#modal-image').modal('show');
				}
			});

			$element.popover('destroy');
		});

		$('#button-clear').on('click', function() {
			$element.find('img').attr('src', $element.find('img').attr('data-placeholder'));

			$element.parent().find('input').val('');

			$element.popover('destroy');
		});

	});

});