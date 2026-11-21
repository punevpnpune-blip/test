# CloudStream Adult Extensions

Independent Kotlin modules for SupJav and SexTB, targeting the CloudStream 4.9.1 Android app. The modules currently register provider identities and are marked available in newly generated plugin indexes. Homepage browsing, pagination, search, metadata, posters, and playback are pending for both providers.

## Build

Install JDK 17, Gradle 8.12, Android SDK Platform 35, and Build Tools 34.0.0. Set `ANDROID_HOME` to your SDK directory or set `sdk.dir` in an untracked `local.properties` file.

```sh
gradle --no-daemon :SupJav:make :SexTB:make :makePluginsJson -PgithubRepository=OWNER/REPOSITORY
```

The CloudStream Gradle plugin writes `SupJav/build/SupJav.cs3`, `SexTB/build/SexTB.cs3`, and `build/plugins.json`. The build uses the official template’s pre-release API stub because the 4.9.1 release does not publish `classes.jar`. Compatibility with the 4.9.1 app still needs a device test.

## GitHub Actions

CI uses Gradle's official setup action to install Gradle 8.12 directly. It installs Temurin JDK 17, Android SDK Platform 35, and Build Tools 34.0.0 on each runner. Gradle, AGP 8.7.3, Kotlin 2.3.0, and JDK 17 match the [official extensions repository](https://github.com/recloudstream/extensions). The CloudStream Gradle plugin is pinned to the JitPack build `81b1d424d2`, which provides the `writeCacheEntry` task used by CI.

The SupJav and SexTB jobs run independently. Each reports its own result and uploads a provider-named artifact containing its CS3 and plugin index entry on success. The assembly job validates both packages, then uploads the combined repository artifact. Publishing requires successful assembly.

## Publish on GitHub

1. Push this source tree to a public GitHub repository with Actions enabled.
2. Open **Actions → Build CloudStream extensions → Run workflow** on the default branch. Select the publish checkbox to publish the development packages.
3. The workflow builds and checks both packages, uploads them as a workflow artifact, and writes the packages and manifests to the `builds` branch. It fills in the real GitHub repository address in the published `repo.json`.

The publishing job uses GitHub Actions’ built-in token with `contents: write`. The `builds` branch must permit pushes from the workflow.

## Install in CloudStream 4.9.1

1. Install [CloudStream 4.9.1](https://github.com/recloudstream/cloudstream/releases/tag/v4.9.1).
2. Open **Settings → Extensions → Add Repository** and enter the published manifest URL, replacing the owner and repository name.

   ```text
   https://raw.githubusercontent.com/OWNER/REPOSITORY/builds/repo.json
   ```

3. Open the added repository. Use the app’s NSFW category settings if you are an adult and the entries are hidden. The entries are development scaffolds with no browse or playback functionality.

## Verification status

| Provider | Public site inspection |
| --- | --- |
| SupJav | The homepage fetch returned HTTP 403. |
| SexTB | The homepage fetch returned HTTP 402. The public FAQ was readable, but it did not expose catalog or player markup. |

To implement each provider, obtain current HTML from its publicly accessible homepage, a later catalog page, a search results page, and a public detail page. Check the public player flow from that detail page before adding playback. Leave out any sources that require authentication, an access-control bypass, or DRM circumvention.

No successful compilation log is available for either provider. The updated GitHub Actions workflow and publishing are unverified. Once CI produces packages, test repository import, installation, plugin loading, and registration on an Android device running CloudStream 4.9.1. Test catalog and playback features after they are implemented.

Project conventions follow the [official CloudStream TestPlugins template](https://github.com/recloudstream/TestPlugins).
