$(function() {

    $('body').delegate('.simple-ajax-upload', 'change', function () {
        var $this = $(this),
            file = this.files[0],
            url = $this.data('url'),
            ajaxRequest = null;

        if (typeof file != 'undefined' && typeof url != 'undefined') {
            var formData = new FormData(),
                // the parent container to obtain the needed HTML elements through it
                closestContainer = (typeof $this.data('closestcontainer') != 'undefined') ? $this.closest($this.data('closestcontainer')) : null,
                // HTML element to add the progress bar
                progressContainer = (closestContainer != null && $this.data('closestcontainer') == $this.data('progresscontainer')) ? closestContainer
                    : (closestContainer == null && typeof $this.data('progresscontainer') != 'undefined') ? $this.closest($this.data('progresscontainer'))
                    : (typeof $this.data('progresscontainer') != 'undefined') ? closestContainer.find($this.data('progresscontainer')) : null,
                // if the closestContainer if not defined then the progressContainer will be the parent container
                closestContainer = (closestContainer == null && progressContainer != null) ? progressContainer : closestContainer,
                // progress element
                proccess = $('<table class="proccess-content col-md-12 padding-none-LR">' +
                                '<tr>' +
                                    '<td class="col-md-11 padding-none-LR"><progress value="0" max="100"></progress></td>' +
                                    '<td class="col-md-1 padding-none-LR"><a href="#" class="abort-upload" style="padding-left: 5px;"><i class="fa fa-times"></i></a></td>' +
                                '</tr>' +
                            '</table>'),
                // event to be called when the request is aborted by the user
                triggerAbortEvent = (typeof $this.data('triggerabortevent') != 'undefined') ? $this.data('triggerabortevent') : null,
                // HTML element that will trigger the triggerAbortEvent
                triggerAbortTarget = (closestContainer != null && typeof $this.data('triggeraborttarget') != 'undefined') ? closestContainer.find($this.data('triggeraborttarget')) : null,
                // to save the temporal file ID
                tempFileId = $this.parent().find('input:hidden.temp_file_id'),

                progressHandlingFunction = function (e) {
                    proccess.find('progress').attr({value:e.loaded, max:e.total});
                };

            if (progressContainer != null) {
                formData.append('file', file);
                ajaxRequest = $.ajax({
                    url: url,
                    type: 'POST',
                    xhr: function() {  // Custom XMLHttpRequest
                        var myXhr = $.ajaxSettings.xhr();
                        if(myXhr.upload){ // Check if upload property exists
                            myXhr.upload.addEventListener('progress', progressHandlingFunction, false); // For handling the progress of the upload
                        }
                        return myXhr;
                    },
                    //Ajax events
                    beforeSend: function (xhr, settings) {
                        // Finds if is POST method
                        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type))) {
                            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                        }

                        if (progressContainer != null) {
                            progressContainer.append(proccess);
                        } else {
                            $this.parent().append(proccess);
                        }
                        // set to empty before send request
                        tempFileId.val("");

                        // Throw a before send event to add another behavior
                        $this.trigger($.Event('beforeSend.media.ajaxUpload', {
                            xhr: xhr,
                            settings: settings
                        }));
                    },
                    success: function(response, status, xhr) {
                        if (status == 'success') {
                            if (response['result']) {
                                // clean the file component in order to avoid sumbit the file again
                                $this.val("");
                                // saving the temporal file ID
                                tempFileId.val(response['object_pk']);

                                // Throw a success event to add another behavior
                                $this.trigger($.Event('success.media.ajaxUpload', {
                                    response: response,
                                    status: status,
                                    xhr: xhr
                                }));
                            } else {
                                $.addNotification($.TOP_LAYOUT, $.ERROR, response['failedMsg']);

                                // Throw a non success event to add another behavior
                                $this.trigger($.Event('nonSuccess.media.ajaxUpload', {
                                    response: response,
                                    status: status,
                                    xhr: xhr
                                }));
                            }
                        }
                    },
                    complete: function(xhr, status) {
                        if (progressContainer != null) {
                            progressContainer.find('.proccess-content').remove();
                        } else {
                            $this.parent().find('.proccess-content').remove();
                        }

                        // Throw a complete event to add another behavior
                        $this.trigger($.Event('complete.media.ajaxUpload', {
                            status: status,
                            xhr: xhr
                        }));
                    },
                    // Form data
                    data: formData,
                    enctype: 'multipart/form-data',
                    //Options to tell jQuery not to process data or worry about content-type.
                    cache: false,
                    contentType: false,
                    processData: false
                });
                // abort button implementaion
                proccess.find('a.abort-upload').click(function () {
                    ajaxRequest.abort();
                    if (triggerAbortEvent != null && triggerAbortTarget != null)
                        // trigger the abort event
                        triggerAbortTarget.trigger(triggerAbortEvent);
                });

                if (triggerAbortEvent != null && triggerAbortTarget != null)
                    // adding other behavior to the triggerAbortTarget
                    triggerAbortTarget.on(triggerAbortEvent, function () {
                        ajaxRequest.abort();
                        tempFileId.val("");
                    });

            } else {
                throw new Error('The progress container must be specified.');
            }
        }
    });
});