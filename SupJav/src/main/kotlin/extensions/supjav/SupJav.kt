package extensions.supjav

import com.lagradost.cloudstream3.MainAPI
import com.lagradost.cloudstream3.SearchResponse
import com.lagradost.cloudstream3.TvType

class SupJav : MainAPI() {
    override var name = "SupJav"
    override var mainUrl = "https://supjav.com"
    override val supportedTypes = setOf(TvType.NSFW)

    override suspend fun search(query: String): List<SearchResponse> = emptyList()
}
