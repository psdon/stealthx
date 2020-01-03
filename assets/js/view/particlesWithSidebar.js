import invokeParticles from '../module/invokeParticles';
import { addEventByElementId, showHide } from '../script';

export default function particlesWithSidebar() {
  invokeParticles('particles');

  addEventByElementId('sb_x_button', 'click', (e) => {
    showHide('sidebar');
    showHide('hamburger');
  })

  addEventByElementId('hamburger', 'click', (e) => {
    showHide('sidebar');
    showHide('hamburger');
  })


}
