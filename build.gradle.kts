import com.android.build.gradle.BaseExtension
import com.lagradost.cloudstream3.gradle.CloudstreamExtension
import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import org.jetbrains.kotlin.gradle.tasks.KotlinJvmCompile

buildscript {
    repositories {
        google()
        mavenCentral()
        maven("https://jitpack.io")
    }
    dependencies {
        classpath("com.android.tools.build:gradle:9.1.1")
        classpath("com.github.recloudstream:gradle:32895aedb6366f5075cb99bbd2e6ce0a7cac325d")
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:2.4.0")
    }
}

val githubRepository = providers.gradleProperty("githubRepository")
    .orElse(providers.environmentVariable("GITHUB_REPOSITORY"))
    .orElse("OWNER/REPOSITORY")

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

fun Project.cloudstream(configure: CloudstreamExtension.() -> Unit) {
    extensions.getByType<CloudstreamExtension>().configure()
}

subprojects {
    apply(plugin = "com.android.library")
    apply(plugin = "kotlin-android")

    extensions.configure<BaseExtension> {
        namespace = "extensions.${project.name.lowercase()}"
        compileSdkVersion(35)
        defaultConfig {
            minSdk = 21
            targetSdk = 35
        }
        compileOptions {
            sourceCompatibility = JavaVersion.VERSION_1_8
            targetCompatibility = JavaVersion.VERSION_1_8
        }
    }

    apply(plugin = "com.lagradost.cloudstream3.gradle")
    cloudstream {
        setRepo(githubRepository.get())
        buildBranch = "builds"
    }

    tasks.withType<KotlinJvmCompile>().configureEach {
        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_1_8)
            freeCompilerArgs.addAll(
                "-Xno-call-assertions",
                "-Xno-param-assertions",
                "-Xno-receiver-assertions",
            )
        }
    }

    dependencies {
        // The 4.9.1 release supplies an APK. The official template uses this API stub.
        add("cloudstream", "com.lagradost:cloudstream3:pre-release")
    }
}
