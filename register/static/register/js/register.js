function togglePaymentFields() {
    var method = document.getElementById('payment_method').value;
    document.getElementById('upiFields').style.display = (method === 'upi') ? 'block' : 'none';
    document.getElementById('qrFields').style.display = (method === 'qr') ? 'block' : 'none';
}
document.addEventListener('DOMContentLoaded', function() {
    togglePaymentFields();
    var form = document.getElementById('registrationForm');
    form.addEventListener('submit', function() {
        form.classList.add('animate-fade-in');
    });
});
