/// @file Terrain.h
/// @brief Manages Terrain-related Rex logic.
/// For conditions of distribution and use, see copyright notice in license.txt
#ifndef incl_Terrain_h
#define incl_Terrain_h

#include "Entity.h"
#include "EC_Terrain.h"
#include "EnvironmentModuleApi.h"

namespace Resource
{
    namespace Events
    {
        class ResourceReady;
    }
}

namespace ProtocolUtilities
{
    class NetworkEventInboundData;
}

namespace Environment
{

struct DecodedTerrainPatch;

//! Handles the logic related to the OpenSim Terrain. Note - partially lacks support for multiple scenes - the Terrain object is not instantiated
//! per-scene, but it contains data that should be stored per-scene. This doesn't affect anything unless we will some day actually have several scenes.
class ENVIRONMENT_MODULE_API Terrain
{
public:
    Terrain(EnvironmentModule *owner_);
    ~Terrain();

    //! Called to handle an OpenSim LayerData packet.
    //! Decodes terrain data from a LayerData packet and generates terrain patches accordingly.
    bool HandleOSNE_LayerData(ProtocolUtilities::NetworkEventInboundData* data);

    //! The OpenSim terrain has a hardcoded size of four textures. When/if we lift that, change the amount here or remove altogether if dynamic.
    static const int num_terrain_textures = 4;

    /// Sets the new terrain texture UUIDs that are used for this terrain. Places
    /// new resource requests to the asset handler if any of the textures have changed.
    void SetTerrainTextures(const RexTypes::RexAssetID textures[num_terrain_textures]);

    void SetTerrainHeightValues(const Real start_heights[num_terrain_textures], const Real height_ranges[num_terrain_textures]);

    void RequestTerrainTextures();

    //! Looks through all the entities in RexLogic's currently active scene to find the Terrain
    //! entity. Caches it internally. Use GetTerrainEntity to obtain it afterwards.
    void FindCurrentlyActiveTerrain();

    //! @return The scene entity that represents the terrain in the currently active world.
    Scene::EntityWeakPtr GetTerrainEntity();

    //! Called whenever a texture is loaded so it can be attached to the terrain.
    void OnTextureReadyEvent(Resource::Events::ResourceReady *tex);

    //! Get terrain texture ids.
    const RexTypes::RexAssetID &GetTerrainTextureID(int index) const;

    const Real &GetTerrainTextureStartHeight(int index) const;

    const Real &GetTerrainTextureHeightRange(int index) const;

private:
    EnvironmentModule *owner_;

    request_tag_t terrain_texture_requests_[num_terrain_textures];

    //! UUID's of the texture assets the terrain uses for rendering. Should be stored per-scene.
    RexTypes::RexAssetID terrain_textures_[num_terrain_textures];

    //! lowest point where the fist texture is blended
    Real start_heights_[num_terrain_textures];
    Real height_ranges_[num_terrain_textures];

    Scene::EntityWeakPtr cachedTerrainEntity_;

    void CreateOrUpdateTerrainPatchHeightData(const DecodedTerrainPatch &patch, int patchSize);

    void RegenerateDirtyTerrainPatches();

    void CreateOgreTerrainPatchNode(Ogre::SceneNode *&node, int patchX, int patchY);

    void GenerateTerrainGeometryForOnePatch(Scene::Entity &entity, EC_Terrain &terrain, EC_Terrain::Patch &patch);
    void GenerateTerrainGeometry(EC_Terrain &terrain);
    void GenerateTerrainGeometryForSinglePatch(EC_Terrain &terrain, int patchX, int patchY);
    void DebugGenerateTerrainVisData(Ogre::SceneNode *node, const DecodedTerrainPatch &patch, int patchSize);

    void SetTerrainMaterialTexture(int index, const char *textureName);
};

}

#endif
