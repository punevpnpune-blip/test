package extensions.sextb

import com.lagradost.cloudstream3.MainAPI
import com.lagradost.cloudstream3.SearchResponse
import com.lagradost.cloudstream3.TvType

class SexTB : MainAPI() {
    override var name = "SexTB"
    override var mainUrl = "https://sextb.net"
    override val supportedTypes = setOf(TvType.NSFW)

    override suspend fun search(query: String): List<SearchResponse> = emptyList()
}
