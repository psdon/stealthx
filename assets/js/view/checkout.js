import invokeParticles from '../module/invokeParticles';

export default function signIn() {
  invokeParticles('particles');

  const monthlyPrice = 300
  let total = document.getElementById("total")

  let monthsInput = document.getElementById("months_plan")
  monthsInput.value = 1
  monthsInput.oninput = () => {
    let calculated_total = monthsInput.value * monthlyPrice
    total.innerHTML = '₱' + calculated_total + ' PHP'
  }
}
