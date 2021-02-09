import time
from google_trans_new import google_translator

from jkPyUtils.icache import cache


translator = google_translator(url_suffix='com')


@cache
def translate(src, sleep_interval=None):
    if sleep_interval:
        time.sleep(sleep_interval)

    translate_text = translator.translate(src, lang_tgt='zh-cn')
    return translate_text


if __name__ == '__main__':
    title = 'Strain-engineered high-responsivity MoTe2 photodetector for silicon photonic integrated circuits'
    abstract = '<p>In integrated photonics, specific wavelengths such as 1,550&#8201;nm are preferred due to low-loss transmission and the availability of optical gain in this spectral region. For chip-based photodetectors, two-dimensional materials bear scientifically and technologically relevant properties such as electrostatic tunability and strong light&#8211;matter interactions. However, no efficient photodetector in the telecommunication C-band has been realized with two-dimensional transition metal dichalcogenide materials due to their large optical bandgaps. Here we demonstrate a MoTe<sub>2</sub>-based photodetector featuring a strong photoresponse (responsivity 0.5&#8201;A&#8201;W<sup>&#8211;1</sup>) operating at 1,550&#8201;nm in silicon photonics enabled by strain engineering the two-dimensional material. Non-planarized waveguide structures show a bandgap modulation of 0.2&#8201;eV, resulting in a large photoresponse in an otherwise photoinactive medium when unstrained. Unlike graphene-based photodetectors that rely on a gapless band structure, this photodetector shows an approximately 100-fold reduction in dark current, enabling an efficient noise-equivalent power of 90&#8201;pW&#8201;Hz<sup>&#8211;</sup><sup>0.5</sup>. Such a strain-engineered integrated photodetector provides new opportunities for integrated optoelectronic systems.</p>'

    title_cn = translate(title)
    abstract_cn = translate(abstract)

    print('title: %s' % title)
    print('title cn: %s' % title_cn)
    print('======')
    print('abstract: %s' % abstract)
    print('abstract cn: %s' % abstract_cn)
