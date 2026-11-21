package extensions.supjav

import android.content.Context
import com.lagradost.cloudstream3.plugins.CloudstreamPlugin
import com.lagradost.cloudstream3.plugins.Plugin

@CloudstreamPlugin
class SupJavPlugin : Plugin() {
    override fun load(context: Context) {
        registerMainAPI(SupJav())
    }
}
