from pdf2image import convert_from_path
import tempfile,os,time
#安装 pip install pdf2image
#安装 brew install poppler

def pdf2images(filename, outputDir):
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
        with tempfile.TemporaryDirectory() as path:
            images = convert_from_path(filename)
            for index, img in enumerate(images):
                img.save('%s/page_%s.png' % (outputDir, index))

def manypdf2images(pdfDir,outDir):
    if not os.path.exists(outDir):
        os.mkdir(outDir)
    files=os.listdir(pdfDir)
    for file in files:
        if file.split('.')[-1] in ['pdf', 'PDF']:
            print( time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),file)
            pdf2images(pdfDir+'/'+file,outDir+'/'+file.split('.')[0])


if __name__ == "__main__":
    # pdf2images('/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(1,199)_ocr/9-1-Civic.pdf', '/Users/brobear/Desktop/9-1')
    manypdf2images('/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(200,499)_ocr',
                   '/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(200,499)_ocr_images')

'''
brew install poppler
。
。
。

==> gettext
gettext is keg-only, which means it was not symlinked into /usr/local,
because macOS provides the BSD gettext library & some software gets confused if both are in the library path.

If you need to have gettext first in your PATH run:
  echo 'export PATH="/usr/local/opt/gettext/bin:$PATH"' >> ~/.bash_profile

For compilers to find gettext you may need to set:
  export LDFLAGS="-L/usr/local/opt/gettext/lib"
  export CPPFLAGS="-I/usr/local/opt/gettext/include"

==> libffi
libffi is keg-only, which means it was not symlinked into /usr/local,
because some formulae require a newer version of libffi.

For compilers to find libffi you may need to set:
  export LDFLAGS="-L/usr/local/opt/libffi/lib"

==> nss
nss is keg-only, which means it was not symlinked into /usr/local,
because Firefox can pick this up instead of the built-in library, resulting in
random crashes without meaningful explanation.

Please see https://bugzilla.mozilla.org/show_bug.cgi?id=1142646 for details.

If you need to have nss first in your PATH run:
  echo 'export PATH="/usr/local/opt/nss/bin:$PATH"' >> ~/.bash_profile

For compilers to find nss you may need to set:
  export LDFLAGS="-L/usr/local/opt/nss/lib"
  export CPPFLAGS="-I/usr/local/opt/nss/include"
'''