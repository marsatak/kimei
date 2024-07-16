export function showDynamicModal(options) {
    const {
        title,
        inputType,
        inputId,
        placeholder,
        confirmButtonText,
        onConfirm
    } = options;

    const modalId = 'dynamicModal-' + Math.random().toString(36).substr(2, 9);

    const modalHtml = `
        <div id="${modalId}" class="modal fade" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                    </div>
                    <div class="modal-body">
                        <input type="${inputType}" id="${inputId}" class="form-control" placeholder="${placeholder}">
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
                        <button type="button" class="btn btn-primary" id="confirmButton">${confirmButtonText}</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    $('body').append(modalHtml);

    const $modal = $(`#${modalId}`);

    $modal.modal('show');

    $modal.find('#confirmButton').on('click', function () {
        const inputValue = $(`#${inputId}`).val();
        $modal.modal('hide');
        onConfirm(inputValue);
    });

    $modal.on('hidden.bs.modal', function () {
        $(this).remove();
    });
}