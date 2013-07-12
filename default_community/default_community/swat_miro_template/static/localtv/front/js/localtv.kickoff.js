;jQuery(function($){
	
	// if a shebang is present in the URI, redirect
	if (window.location.hash.search('#!') === 0) {
		window.location = window.location.href.replace(/#!/g,'')
	}
	
	// start anything which has a [data-cycle] attribute cycling
	$('.carousel').each(function(){
		var $this = $(this),
			pager = $('<div class="carousel-pager"></div>').appendTo($this.parent());
		$this.cycle({
			fx: 'scrollUp',
			pause: true, // pause on hover
			timeout: 6000, // 6 seconds between slides
			pager: pager,
			pauseOnPagerHover: true,
			slideResize: false,
			containerResize: false,
			slideExpr: '.video-large'
		});
	});
	
	// shrinkydink all .video-details classes
	$('.video-details').shrinkydink();
	
	// add popovers to things
	// the placement function calculates the placement of the popover,
	// defaulting to right and switching to left if the popover is too close
	// to the edge.
	$('body').popover({selector: '.popover-trigger', placement: function (element) {
		var position = this.getPosition();
		// distance from edge of hover element + width of hover element + width of popover
		return (position.left + position.width + 300 > $(window).width()) ? 'left' : 'right';
	}});
	
	// Infinite Scroll
	// Only triggered if a `body.video-list-page` exists and we're on the first page
	// TODO: handle the case where we are not on the first page.
	if ($('body').hasClass('video-list-page') && $('.pagetabs').find('li:first').hasClass('selected')) {
		$('.pagetabs').hide(); // hide pagination
		// preload the ajax loader image
		var ajax_image = new Image();
		ajax_image.src = STATIC_URL + "localtv/front/images/ajax-loader.gif";
		// kick off the infinite scrolling
		$('.video-grid').infinitescroll({
			loading: {
				img: null,
				// override a lot of the default behavior
				finished: function (opts) {
					var $this = $(this);
					window.location.hash = "#!?page=" + opts.state.currPage;
					$('#infscr-loading').remove(); // hide the spinner
					$this.infinitescroll('pause'); // prevent from loading the next page
					if ($this.data('infscr_first_load') !== 'done'){
						// if this is the first load, create a next page button
						$this.data('infscr_first_load', 'done');
						var next_page_button =$('<a href="#" class="button button-wide">Load More Videos</a>');
						$this.data('infscr_next_button', next_page_button);
						next_page_button.click(function (e) {
							$(this).hide();
							$this.infinitescroll('resume');
							e.preventDefault();
						});
						$this.after(next_page_button);
					} else {
						$this.data('infscr_next_button').show();
					}
				},
				start: function (opts) {
					opts.loading.msg = $("<li class=\"media-item loading\" id=\"infscr-loading\">Loading&hellip;</li>")
					$(opts.navSelector).hide();
					opts.loading.msg
						.appendTo(opts.loading.selector)
						.show(opts.loading.speed, function () {
							beginAjax(opts);
						});
				}
			},
			errorCallback: function (error) {
				if(error === "done"){
					var $infscrLoading = $('#infscr-loading');
					$infscrLoading.after("<li class=\"media-item done\" id=\"infscr-done\">End of Videos</li>");
					$infscrLoading.remove();
					$this.data('infscr_next_button').remove();
				}
			},
			navSelector: '.pagetabs',
			nextSelector: '.pagetabs > .selected + li > a',
			itemSelector: '.media-item'
		});
	};
	
	// Dropdowns
	$('.nav-item-dropdown').dropdown()
	//$('body').on('mouseover.localtv.dropdown', '.nav-item-dropdown', function (e) {
		//$(this).dropdown('show')
	//});
	$('html').click(function() {
		$('.nav-item-dropdown').dropdown('hide');
		$('.nav-item-dropdown > a').css('color', '#EEEEEE');
	});
	$('.nav-item-dropdown').click(function() {
		$('.nav-item-dropdown').dropdown('hide');
		$('.nav-item-dropdown > a').css('color', '#EEEEEE');
	});
	$('body').on('click.localtv.dropdown', '.nav-item-dropdown', function (event) {
		event.stopPropagation();
		if($(this).hasClass('open')){
			$(this).dropdown('hide');
			$('a', this).css('color', '#EEEEEE');
		}
		else{
			$(this).dropdown('show');
			$('a', this).css('color', '#444444');
		}
	});
	//$('body').on('mouseout.localtv.dropdown', '.nav-item-dropdown', function (e) {
		//$(this).dropdown('hide')
	//});
	
});