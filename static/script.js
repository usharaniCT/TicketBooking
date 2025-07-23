
function showConfirmation(event) {
  event.preventDefault();
  const confirmBooking = confirm("Do you want to confirm your ticket booking?");
  if (confirmBooking) {
    document.getElementById("bookingForm").submit();
  }
}
