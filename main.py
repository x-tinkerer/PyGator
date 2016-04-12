import form
from optparse import OptionParser

if __name__ == "__main__":
    usage = "usage: %prog [-d device][-t target]"
    parser = OptionParser()
    parser.add_option('-t', '--target', dest="target",
                      help="The test app name,"
                           "will use to create folder for this APP.",
                      default="", type="string")

    parser.add_option('-d', '--device', dest="platform",
                      help="The target phone platform, M86/M80/M95 etc.",
                      type="string")

    (options, args) = parser.parse_args()

    plat = options.platform
    appName = options.target

    form.form_main(plat, appName)
