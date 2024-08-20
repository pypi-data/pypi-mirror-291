window.Modal = class {
    constructor({
        url,
        selector,
        $target,
        onSuccess,
        onFormRender,
        onModalRender,
        onCancel,
        focusOn,
        traditional = false,
        contentGetter = (response) => response
    }) {
        this._url = url;
        this._isSubmited = false;
        this._onCancel = onCancel;
        this._traditional = traditional;
        this._focusOn = focusOn;
        this._onSuccess = onSuccess;
        this._onFormRender = onFormRender;
        this._onModalRender = onModalRender;
        this._contentGetter = contentGetter;

        if (selector) {
            $('body').on('click', selector, this.show);
        }

        if ($target && $target.length) {
            const url = $target.data('url');
            if (url) {
                this._url = url;
            }
            $target.click(this.show);
        }
    }

    show = (event) => {
        let url;
        if (typeof this._url === 'function') {
            url = this._url($(event.currentTarget));
        } else {
            url = this._url;
        }
        return $.get(url, (response) => this._renderModal(response, url));
    };

    _renderModal = (response, url) => {
        const content = this._contentGetter(response);
        const $modal = $(content);

        $("body").append($modal);

        $modal.modal("show");
        
        if (this._focusOn) {
            setTimeout(() => $modal.find(this._focusOn).focus(), 500);
        }

        if (this._onModalRender) {
            this._onModalRender($modal, response);
        }

        if (this._onFormRender) {
            this._onFormRender($modal, response);
        }

        $modal.on('submit', 'form', (event) => this._handleFormSubmit(event, url));

        $modal.on('click', '[data-role=submit-btn]', this._handleSubmitBtnClick);

        $modal.on('hidden.bs.modal', this._removeModal);
        
        this._$modal = $modal;
    }
    
    _handleFormSubmit = (event, url) => {

        event.preventDefault();
    
        this._toggleSubmitBtn(false);

        console.log(url)
    
        $(event.target).ajaxSubmit({
            method: 'POST',
            url: url,
            success: this._handleFormSubmitSuccess,
            error: this._handleFormSubmitError,
            traditional: this._traditional,
            complete: () => this._toggleSubmitBtn(true)
        });
    
    }

    _handleFormSubmitSuccess = (response) => {

        this._isSubmited = false;
        this._$modal.modal('hide');

        if ($.notify && response.message) {
            $.notify({message: response.message}, {type: 'success'});
        }

        if (response.url) {
            window.location = response.url
        }

        if (this._onSuccess) {
            this._onSuccess(response);
        }
    }

    _handleFormSubmitError = (response) => {
        this._$modal.find('form').replaceWith(response.responseText);

        if (this._onFormRender) {
            this._onFormRender(this._$modal, response);
        }
    }

    _toggleSubmitBtn = (isActive) => {
        this._$modal.find('[data-role=submit-btn]').prop('disabled', !isActive);
    }

    _handleSubmitBtnClick = () => {
        this._$modal.find('form').submit();
    }

    _removeModal = () => {
        this._$modal.remove();
        if (!this._isSubmited && this._onCancel) {
            this._onCancel();
        }
    }
}
