$(function() {

    $('body').delegate('.fileinput.simple-ajax-upload', 'change.bs.fileinput', function () {
        var $this = $(this),
            element = $this.find(':file'),
            file = element[0].files[0],
            url = element.data('url'),
            // function or variable to check file validation
            validation = element.data('validation'),
            ajaxRequest = null,
            // determines if the proccess can be continued
            executeRequest = (typeof validation == 'undefined') ? true
                : ($.isFunction(eval(validation))) ? eval(eval(validation)(element[0])) : eval(validation);

        if (executeRequest) {
            if (typeof file != 'undefined' && typeof url != 'undefined') {
                var formData = new FormData(),
                    // the parent container to obtain the needed HTML elements through it
                    closestContainer = (typeof element.data('closestcontainer') != 'undefined') ? element.closest(element.data('closestcontainer')) : null,
                    // HTML element to add the progress bar
                    progressContainer = (closestContainer != null && element.data('closestcontainer') == element.data('progresscontainer')) ? closestContainer
                        : (closestContainer == null && typeof element.data('progresscontainer') != 'undefined') ? element.closest(element.data('progresscontainer'))
                        : (typeof element.data('progresscontainer') != 'undefined') ? closestContainer.find(element.data('progresscontainer')) : null,
                    // if the closestContainer if not defined then the progressContainer will be the parent container
                    closestContainer = (closestContainer == null && progressContainer != null) ? progressContainer : closestContainer,
                    // progress element
                    proccess = $('<table class="proccess-content col-md-12 padding-none-LR">' +
                                    '<tr>' +
                                        '<td class="col-md-11 padding-none-LR"><progress value="0" max="100"></progress></td>' +
                                        '<td class="col-md-1 padding-none-LR"><a href="#" class="abort-upload" style="padding-left: 5px;"><i class="fa fa-times"></i></a></td>' +
                                    '</tr>' +
                                '</table>'),
                    // to save the temporal file ID
                    tempFileId = element.parent().find('input:hidden.temp_file_id'),

                    progressHandlingFunction = function (e) {
                        proccess.find('progress').attr({value:e.loaded, max:e.total});
                    };

                if (progressContainer != null) {
                    formData.append('file', file);
                    // getting file mime type
                    var mimeType = element.data('contentvalidation');
                    // append the mime type to the form data
                    if (mimeType != 'undefined') formData.append('content', mimeType);

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
                            // Throw a before send event to add another behavior
                            element.trigger($.Event('beforeSend.media.ajaxUpload', {
                                xhr: xhr,
                                settings: settings
                            }));

                            // Finds if is POST method
                            if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type))) {
                                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                            }

                            if (progressContainer != null) {
                                progressContainer.append(proccess);
                            } else {
                                element.parent().append(proccess);
                            }
                            // set to empty before send request
                            tempFileId.val("");
                        },
                        success: function(response, status, xhr) {
                            if (status == 'success') {
                                if (response['result']) {
                                    // clean the file component in order to avoid sumbit the file again
                                    element.val("");
                                    // saving the temporal file ID
                                    tempFileId.val(response['object_pk']);
                                    // Throw a success event to add another behavior
                                    element.trigger($.Event('success.media.ajaxUpload', {
                                        response: response,
                                        status: status,
                                        xhr: xhr
                                    }));
                                } else {
                                    $.each(response['failedMsgs'], function(i, msg) {
                                      $.addNotification($.TOP_LAYOUT, $.ERROR, msg);
                                    });
                                    // Throw a non success event to add another behavior
                                    element.trigger($.Event('nonSuccess.media.ajaxUpload', {
                                        response: response,
                                        status: status,
                                        xhr: xhr
                                    }));
                                    // cleans the bootstrap fileinput component
                                    $this.fileinput('clear');
                                }
                            }
                        },
                        complete: function(xhr, status) {
                            if (progressContainer != null) {
                                progressContainer.find('.proccess-content').remove();
                            } else {
                                element.parent().find('.proccess-content').remove();
                            }
                            // Throw a complete event to add another behavior
                            element.trigger($.Event('complete.media.ajaxUpload', {
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
                        // cleans the bootstrap fileinput component
                        $this.fileinput('clear');
                    });

                    $this.on('clear.bs.fileinput', function () {
                        ajaxRequest.abort();
                        tempFileId.val("");
                    })

                } else {
                    throw new Error('The progress container must be specified.');
                }
            }
        }
    });
});