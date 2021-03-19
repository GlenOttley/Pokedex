
/*Downloaded from https://www.codeseek.co/shelune/pokemon-red-pokedex-entry-pbgOZq */
$('.lower__content p').click(function () {
  if ($(this).css('display') != 'none') {
    $(this).css('display', 'none').siblings().css('display', 'block');
  }
});