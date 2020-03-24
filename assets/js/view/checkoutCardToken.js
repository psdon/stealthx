import invokeParticles from '../module/invokeParticles';

export default function signIn() {
  invokeParticles('particles');

  const tokenPrice = window.tp
  let total = document.getElementById("total")

  let tokenInput = document.getElementById("token")

  /*Init Default*/
  let calculated_total = tokenInput.value * tokenPrice
  total.innerHTML = '₱' + calculated_total + ' PHP'

  tokenInput.oninput = () => {
    let calculated_total = tokenInput.value * tokenPrice
    total.innerHTML = '₱' + calculated_total + ' PHP'
  }
}
